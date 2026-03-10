# read_all_ft
Repository with code to read DDR ALL_FT+ into pandas dataframe.

This repository provides a library with basic functions to read an ALL_FT+ file and create a dataframe.

## Usage

Install dependencies:

```
pip install pandas py7zr
```

py7zr is optional if your files are not in `.7z` format.

Then import:
```python
from read_all_ft.read_all_ft_functions import read_all_ft_formatted
```

Main function is `read_all_ft_formatted`:
```python
df = read_all_ft_formatted(path_to_all_ft_plus_file)
```

which returns nicely formatted columns. The file can uncompressed, or in the following formats:
`.zip`, `.gz`, `.bz2`, `.xz`, `.7z`. The function will automatically detect the format.

The function `read_all_ft_formatted` also had a flag `convert_datetimes`, True by default. If True, all time columns are 
returned as `datetime` or `timedelta` objects, not strings.

If you need, you can use the low-level functions:
- read_all_ft to read an ALL_FT+ file and create a dataframe with only strings.
- format_all_ft which given a dataframe read with read_all_ft formats the columns.

airac can be passed as a parameter to add the AIRAC to the dataframe as a column.

columns can be passed as a parameter and only those columns are read from the files (faster and lower memory).

`read_all_ft_folder` allows for all files inside a folder to be read and returned in one single dataframe. Files read in parallel.

See main_example_read.py for an example on how to use the library.

## Licence
The library is released under the GPL v3 licence. The licence can be found in LICENCE.TXT