from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import read_all_ft.ddr_headers as ddrh

__version__ = 6.0

def read_all_ft_formatted(allft_path, airace=None, convert_datetimes=True):
    """
    Main function with formatting for convenience. Use read_all_ft if you don't want formatting.
    """
    data, ddr_version = read_all_ft(allft_path, airace)
    return format_all_ft(data, ddr_version, convert_datetimes=convert_datetimes)

# READ ALL_FT+ FILES

def read_all_ft(allft_path, airac=None):
    # Detect if the file is compressed
    allft_path = Path(allft_path)

    extension = str(allft_path).split('.')[-1]
    # print('Extension:', extension)

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

    # For DDR version
    lpos = max(str(allft_path).rfind('\\'), str(allft_path).rfind('/'))
    ddr_source = str(allft_path)[lpos + 1:]
    if compression in ['zip', 'gzip', 'bz2', 'xz']:
        ddr_version_dat = pd.read_csv(allft_path, nrows=1, header=None, compression=compression)

        # Reading data
        data = pd.read_csv(allft_path, sep=";", skiprows=1, header=None, compression=compression)
    elif compression == '7z':
        import py7zr
        from io import StringIO, BytesIO

        with py7zr.SevenZipFile(allft_path, mode='r') as z:
            # print('Decompressing ALLFT+ file from .7z archive...')
            new_name = str(allft_path.stem)

            file_content = z.read(targets=[new_name])[new_name]

            # file_content_bytes = BytesIO(file_content)
            file_content_str = file_content.read().decode('utf-8')

            csv_content = StringIO(file_content_str)

            # # Convert the file content to a StringIO object
            # csv_content = StringIO(file_content_str)

            # Convert the file content to a StringIO object
            # csv_content = StringIO(file_content.decode('utf-8'))

            # READ FILE WITH TRAFFIC DATA AND CREATE PANDA STRUCTURE WITH HEADER OF DDR
            ddr_version_dat = pd.read_csv(csv_content, nrows=1, header=None)
            data = pd.read_csv(csv_content, sep=";", skiprows=1, header=None)
    else:
        ddr_version_dat = pd.read_csv(allft_path, nrows=1, header=None)

        # Reading data
        data = pd.read_csv(allft_path, sep=";", skiprows=1, header=None)

    ddr_version = ddr_version_dat.iloc[0, 0]

    h_ddrv2, h_ddrv3, h_ddrv4, h_ddrv6, h_ddrv8 = ddrh.ddr_headers()

    if ddr_version == 6:
        data.columns = h_ddrv6
    elif ddr_version == 8:
        data.columns = h_ddrv8
    elif ddr_version == 4 or ddr_version == 5:
        data.columns = h_ddrv4
        for i in list(set(h_ddrv6) - set(h_ddrv4)):
            data[i] = None
    elif ddr_version == 3:
        data.columns = h_ddrv3
        for i in list(set(h_ddrv4) - set(h_ddrv3)):
            data[i] = None
    elif ddr_version == 2:
        data.columns = h_ddrv2
        for i in list(set(h_ddrv4) - set(h_ddrv3)):
            data[i] = None
        for i in list(set(h_ddrv3) - set(h_ddrv2)):
            data[i] = None
            
    data['airac'] = airac
    data['ddr_version'] = ddr_version
    data['ddr_source'] = ddr_source

    return data, ddr_version


def format_all_ft(data, ddr_version, convert_datetimes=False):
    # FORMATTING OF DDR DATA IN PANDA TABLE

    # These ones in ddr2 are only hhmmss while in ddr3 are dateandhms
    if ddr_version == 2:
        add_iobt_date(data, 'cdm_early_ttot')
        add_iobt_date(data, 'cdm_ao_ttot')
        add_iobt_date(data, 'cdm_atc_ttot')
        add_iobt_date(data, 'cdm_sequenced_ttot')
        add_iobt_date(data, 'cdm_no_slot_before')
        
    data['aobt'] = data['aobt'].apply(date_formatting)
    data['iobt'] = data['iobt'].apply(date_formatting)
    data['cobt'] = data['cobt'].apply(date_formatting)
    data['eobt'] = data['eobt'].apply(date_formatting)
    data['lobt'] = data['lobt'].apply(date_formatting)
    data['sam_ctot'] = data['sam_ctot'].apply(date_formatting)
    data['sip_ctot'] = data['sip_ctot'].apply(date_formatting)
    data['last_sent_proposal_message'] = data['last_sent_proposal_message'].apply(date_formatting)
    data['last_sent_slot_message'] = data['last_sent_slot_message'].apply(date_formatting)
    data['intention_edition_date'] = data['intention_edition_date'].apply(date_formatting)
    data['cdm_early_ttot'] = data['cdm_early_ttot'].apply(date_formatting)
    data['cdm_ao_ttot'] = data['cdm_ao_ttot'].apply(date_formatting)
    data['cdm_atc_ttot'] = data['cdm_atc_ttot'].apply(date_formatting)
    data['cdm_sequenced_ttot'] = data['cdm_sequenced_ttot'].apply(date_formatting)
    data['cdm_no_slot_before'] = data['cdm_no_slot_before'].apply(date_formatting)

    if convert_datetimes:
        data['aobt'] = data['aobt'].apply(to_datetime)
        data['iobt'] = data['iobt'].apply(to_datetime)
        data['cobt'] = data['cobt'].apply(to_datetime)
        data['eobt'] = data['eobt'].apply(to_datetime)
        data['lobt'] = data['lobt'].apply(to_datetime)
        data['sam_ctot'] = data['sam_ctot'].apply(to_datetime)
        data['sip_ctot'] = data['sip_ctot'].apply(to_datetime)
        data['last_sent_proposal_message'] = data['last_sent_proposal_message'].apply(to_datetime)
        data['last_sent_slot_message'] = data['last_sent_slot_message'].apply(to_datetime)
        data['intention_edition_date'] = data['intention_edition_date'].apply(to_datetime)
        data['cdm_early_ttot'] = data['cdm_early_ttot'].apply(to_datetime)
        data['cdm_ao_ttot'] = data['cdm_ao_ttot'].apply(to_datetime)
        data['cdm_atc_ttot'] = data['cdm_atc_ttot'].apply(to_datetime)
        data['cdm_sequenced_ttot'] = data['cdm_sequenced_ttot'].apply(to_datetime)
        data['cdm_no_slot_before'] = data['cdm_no_slot_before'].apply(to_datetime)


    data['late_filer'] = data['late_filer'].apply(yes_no_binary)
    data['late_updater'] = data['late_updater'].apply(yes_no_binary)
    data['north_atlantic_flight_status'] = data['north_atlantic_flight_status'].apply(yes_no_binary)
    data['sensitive_flight'] = data['sensitive_flight'].apply(yes_no_binary)
    data['sam_sent'] = data['sam_sent'].apply(yes_no_binary)
    data['sip_sent'] = data['sip_sent'].apply(yes_no_binary)
    data['slot_forced'] = data['slot_forced'].apply(yes_no_binary)
    data['ready_for_improvement'] = data['ready_for_improvement'].apply(yes_no_binary)
    data['ready_to_depart'] = data['ready_to_depart'].apply(yes_no_binary)
    data['cdm_off_block_time_discrepancy'] = data['cdm_off_block_time_discrepancy'].apply(yes_no_binary)
    data['intention_flight'] = data['intention_flight'].apply(yes_no_binary)

    data['cdm_taxi_time'] = data['cdm_taxi_time'].apply(time_elapsed_formatting)

    if convert_datetimes:
        data['cdm_taxi_time'] = data['cdm_taxi_time'].apply(to_timedelta)

    return data


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
