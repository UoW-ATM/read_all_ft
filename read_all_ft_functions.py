from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import read_all_ft.ddr_headers as ddrh

__version__ = 7.0


# ==============================================================================
# HELPER: safe column formatter (skips columns that were filtered out)
# ==============================================================================

def _apply_if_exists(data, col, func):
    """Apply a formatting function only if the column exists in the dataframe."""
    if col in data.columns:
        data[col] = data[col].apply(func)


# ==============================================================================
# PUBLIC API
# ==============================================================================

def read_all_ft_formatted(allft_path, airac=None, convert_datetimes=True, columns=None):
    """
        Read a single ALL_FT+ file and return a formatted dataframe.

        Parameters
        ----------
        allft_path : str or Path
            Path to the ALL_FT+ file. Supports .zip, .gz, .bz2, .xz, .7z, and uncompressed.
        airac : str, optional
            AIRAC identifier added as a column.
        convert_datetimes : bool, optional
            If True, convert datetime columns to Python datetime objects. Default True.
        columns : list, optional
            List of column names to keep. If None, all columns are kept.
            Filtering happens before formatting for performance — only kept columns
            are formatted.

        Returns
        -------
        pd.DataFrame
        """
    data, ddr_version = read_all_ft(allft_path, airac, columns=columns)
    return format_all_ft(data, ddr_version, convert_datetimes=convert_datetimes)


def read_all_ft_folder(folder_path, airac=None, formatted=True, convert_datetimes=True,
                       columns=None, n_workers=None, parallel_backend='thread'):
    """
    Read all ALL_FT+ files in a folder and return a concatenated dataframe.

    Reads all files raw (with optional column filtering) first, concatenates,
    then formats once — avoiding redundant formatting passes.

    Parameters
    ----------
    folder_path : str or Path
        Path to folder containing ALL_FT+ files.
    airac : str, optional
        AIRAC identifier passed to read_all_ft. If None, the filename is used
        (default behaviour of read_all_ft).
    formatted : bool, optional
        If True, apply format_all_ft to the final concatenated dataframe. Default True.
    convert_datetimes : bool, optional
        If True and formatted=True, convert datetime columns. Default True.
    columns : list, optional
        List of column names to keep. Filtering happens at read time so unwanted
        columns are never loaded into memory.
    n_workers : int, optional
        Number of parallel workers. Defaults to min(4, number of files).
        Set to 1 to disable parallelism (useful for debugging).
    parallel_backend : str, optional
        'thread' (default) or 'process'. Threads share memory and avoid
        pickling overhead; processes can bypass the GIL but require pickling.
        For I/O-bound workloads (reading large files) threads are usually faster.

    Returns
    -------
    pd.DataFrame
        Concatenated dataframe of all files found in the folder.
    """
    folder_path = Path(folder_path)

    valid_extensions = {'.zip', '.gz', '.bz2', '.xz', '.7z', '.csv', '.ALL_FT+'}
    for f in sorted(folder_path.iterdir()):
        files = [f for f in sorted(folder_path.iterdir())
             if f.is_file() and (f.suffix in valid_extensions or '.' not in f.name)]

    if not files:
        raise ValueError(f"No valid ALL_FT+ files found in {folder_path}")

    n_workers = n_workers or min(4, len(files))

    print(f"Found {len(files)} file(s). Reading with {n_workers} worker(s)...")

    raw_dataframes = []

    def _read(f):
        return read_all_ft(f, airac, columns=columns)

    if n_workers > 1:
        Executor = ThreadPoolExecutor if parallel_backend == 'thread' else ProcessPoolExecutor
        with Executor(max_workers=n_workers) as executor:
            futures = {executor.submit(_read, f): f for f in files}
            for future in as_completed(futures):
                f = futures[future]
                try:
                    data, _ = future.result()
                    raw_dataframes.append(data)
                    print(f"  ✓ {f.name} ({len(data):,} rows)")
                except Exception as e:
                    print(f"  ✗ {f.name} failed: {e}")
    else:
        for f in files:
            try:
                data, _ = _read(f)
                raw_dataframes.append(data)
                print(f"  ✓ {f.name} ({len(data):,} rows)")
            except Exception as e:
                print(f"  ✗ {f.name} failed: {e}")

    if not raw_dataframes:
        raise ValueError("No files could be read successfully.")

    print("Concatenating...")
    combined = pd.concat(raw_dataframes, ignore_index=True)

    # Use ddr_version from the first successfully read file
    ddr_version = combined['ddr_version'].iloc[0]

    if formatted:
        print("Formatting...")
        combined = format_all_ft(combined, ddr_version, convert_datetimes=convert_datetimes)

    print(f"Done. Final dataframe: {len(combined):,} rows x {len(combined.columns)} columns.")
    return combined


# ==============================================================================
# CORE READ
# ==============================================================================

def read_all_ft(allft_path, airac=None, columns=None):
    """
    Read a single ALL_FT+ file and return a raw (unformatted) dataframe.

    Parameters
    ----------
    allft_path : str or Path
        Path to the ALL_FT+ file.
    airac : str, optional
        AIRAC identifier added as a column.
    columns : list, optional
        List of column names to keep after reading. If None, all columns are kept.
        Filtering is applied immediately after headers are assigned, so memory
        usage is reduced as early as possible.

    Returns
    -------
    tuple : (pd.DataFrame, int)
        The data and the DDR version number.
    """
    allft_path = Path(allft_path)

    extension = str(allft_path).split('.')[-1]

    if extension == 'zip':
        # File is compressed, and the compression is supported by pandas natively
        compression = 'zip'
    elif extension == 'gz':
        # File is compressed, and the compression is supported by pandas natively
        compression = 'gzip'
    elif extension == 'bz2':
        # File is compressed, and the compression is supported by pandas natively
        compression = 'bz2'
    elif extension == 'xz':
        # File is compressed, and the compression is supported by pandas natively
        compression = 'xz'
    elif extension == '7z':
        # File is compressed, but pandas does not support 7z decompression natively
        compression = '7z'
    else:
        compression = None

    # For DDR source name
    lpos = max(str(allft_path).rfind('\\'), str(allft_path).rfind('/'))
    ddr_source = str(allft_path)[lpos + 1:]

    # ------------------------------------------------------------------
    # Step 1: read only the first row to get the DDR version
    # ------------------------------------------------------------------
    if compression in ['zip', 'gzip', 'bz2', 'xz']:
        ddr_version_dat = pd.read_csv(allft_path, nrows=1, header=None, compression=compression)
    elif compression == '7z':
        import py7zr
        import os
        from io import StringIO
        import tempfile

        # Extract to a temp dir — reused for the data read below
        _tmp_dir = tempfile.mkdtemp()
        with py7zr.SevenZipFile(allft_path, mode='r') as z:
            z.extractall(path=_tmp_dir)
        _extracted_file = os.path.join(_tmp_dir, str(allft_path.stem))

        with open(_extracted_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        ddr_version_dat = pd.read_csv(StringIO(first_line), nrows=1, header=None)
    else:
        ddr_version_dat = pd.read_csv(allft_path, nrows=1, header=None)

    ddr_version = ddr_version_dat.iloc[0, 0]

    # ------------------------------------------------------------------
    # Step 2: resolve the correct header list for this DDR version
    # ------------------------------------------------------------------
    h_ddrv2, h_ddrv3, h_ddrv4, h_ddrv6, h_ddrv8 = ddrh.ddr_headers()

    _version_headers = {
        2: h_ddrv2,
        3: h_ddrv3,
        4: h_ddrv4,
        5: h_ddrv4,
        6: h_ddrv6,
        8: h_ddrv8,
    }
    header_list = _version_headers.get(ddr_version, h_ddrv6)

    # ------------------------------------------------------------------
    # Step 3: build usecols as integer indices so pandas skips unwanted
    #         columns at parse time (works with header=None CSVs)
    # ------------------------------------------------------------------
    if columns is not None:
        missing = [c for c in columns if c not in header_list]
        if missing:
            print(f"  Warning: requested columns not found and will be ignored: {missing}")
        col_indices = [i for i, h in enumerate(header_list) if h in columns]
        kept_headers = [header_list[i] for i in col_indices]
    else:
        col_indices = None  # read all columns
        kept_headers = header_list

    # ------------------------------------------------------------------
    # Step 4: read the actual data, skipping unwanted columns at parse time
    # ------------------------------------------------------------------
    _read_kwargs = dict(sep=";", skiprows=1, header=None, usecols=col_indices)

    if compression in ['zip', 'gzip', 'bz2', 'xz']:
        data = pd.read_csv(allft_path, compression=compression, **_read_kwargs)
    elif compression == '7z':
        # Reuse the already-extracted temp file
        data = pd.read_csv(_extracted_file, **_read_kwargs)
        # Clean up temp dir now we're done with it
        import shutil
        shutil.rmtree(_tmp_dir, ignore_errors=True)
    else:
        data = pd.read_csv(allft_path, **_read_kwargs)

    # ------------------------------------------------------------------
    # Step 5: assign column names for the kept columns
    # ------------------------------------------------------------------
    data.columns = kept_headers

    # For older DDR versions, add missing columns as None so downstream
    # code always finds the expected fields (only if not filtered out)
    if ddr_version in (4, 5):
        for col in set(h_ddrv6) - set(h_ddrv4):
            if columns is None or col in columns:
                data[col] = None
    elif ddr_version == 3:
        for col in set(h_ddrv4) - set(h_ddrv3):
            if columns is None or col in columns:
                data[col] = None
    elif ddr_version == 2:
        for col in set(h_ddrv4) - set(h_ddrv3):
            if columns is None or col in columns:
                data[col] = None
        for col in set(h_ddrv3) - set(h_ddrv2):
            if columns is None or col in columns:
                data[col] = None

    # Metadata columns — always kept regardless of columns filter
    data['airac'] = airac
    data['ddr_version'] = ddr_version
    data['ddr_source'] = ddr_source

    return data, ddr_version


# ==============================================================================
# FORMATTING
# ==============================================================================

def format_all_ft(data, ddr_version, convert_datetimes=False):
    """
    Format a raw ALL_FT+ dataframe in place.
    Columns that were filtered out before this call are safely skipped.
    """
    # DDR v2 special case: some time fields are hhmmss only, need date prepended
    if ddr_version == 2:
        add_iobt_date(data, 'cdm_early_ttot')
        add_iobt_date(data, 'cdm_ao_ttot')
        add_iobt_date(data, 'cdm_atc_ttot')
        add_iobt_date(data, 'cdm_sequenced_ttot')
        add_iobt_date(data, 'cdm_no_slot_before')

    # Datetime columns
    _datetime_cols = [
        'aobt', 'iobt', 'cobt', 'eobt', 'lobt',
        'sam_ctot', 'sip_ctot',
        'last_sent_proposal_message', 'last_sent_slot_message',
        'intention_edition_date',
        'cdm_early_ttot', 'cdm_ao_ttot', 'cdm_atc_ttot',
        'cdm_sequenced_ttot', 'cdm_no_slot_before',
    ]
    for col in _datetime_cols:
        _apply_if_exists(data, col, date_formatting)

    if convert_datetimes:
        for col in _datetime_cols:
            _apply_if_exists(data, col, to_datetime)

    # Binary (Y/N) columns
    _binary_cols = [
        'late_filer', 'late_updater', 'north_atlantic_flight_status',
        'sensitive_flight', 'sam_sent', 'sip_sent', 'slot_forced',
        'ready_for_improvement', 'ready_to_depart',
        'cdm_off_block_time_discrepancy', 'intention_flight',
    ]
    for col in _binary_cols:
        _apply_if_exists(data, col, yes_no_binary)

    # Taxi time
    _apply_if_exists(data, 'cdm_taxi_time', time_elapsed_formatting)
    if convert_datetimes:
        _apply_if_exists(data, 'cdm_taxi_time', to_timedelta)

    return data


# ==============================================================================
# FORMATTING HELPERS
# ==============================================================================

# FORMATING DDR DATA
def date_formatting(x):
    if pd.isnull(x):
        return x
    else:
        y = str(x)
        return y[0:4]+"-"+y[4:6]+"-"+y[6:8]+" "+y[8:10]+":"+y[10:12]+":"+y[12:14]


def time_elapsed_formatting(x):
    if pd.isnull(x):
        return x
    else:
        y = str(int(x))
        minutes = int(y[0:-2])
        hours = int(minutes/60)
        minutes = minutes - (hours*60)

        if hours > 9:
            hourss = str(hours)
        else:
            hourss = "0"+str(hours)
        
        if minutes > 9:
            minutess = str(minutes)
        else:
            minutess = "0"+str(minutes)
        return hourss+":"+minutess+":"+y[-2:]
        # return "00:"+y[0:-2]+":"+y[-2:]


def add_iobt_date(ds, field):
    for index, row in ds.iterrows():
        if (not pd.isnull(row['iobt'])) and (not pd.isnull(row[field])):
            date = str(row['iobt'])[:8]
            time = str(int(row[field]))
            while len(time) < 6:
                time = '0'+time
            ds.set_value(index, field, date+time)
             

def yes_no_binary(x):
    if pd.isnull(x):
        return x
    elif x == 'Y':
        return 1
    else:
        return 0


def to_datetime(string):
    if type(string) is float:
        return None
    else:
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def to_timedelta(string):
    if pd.isnull(string):
        return string
    else:
        t = datetime.strptime(string,"%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        return delta
