# read_all_ft
Repository with code to read DDR ALL_FT+ into pandas dataframe.

This repository provides a library with basic functions to read an ALL_FT+ file and create a dataframe.


## Capacities of library

The library (read_all_ft_functions.py) provides 
two main functions:

- read_all_ft to read an ALL_FT+ file and create a dataframe
- format_all_ft which given a dataframe read with read_all_ft formats the columns.

read_all_ft function which expects the path to the ALL_FT+ file and returns a dataframe with the information on the file. It automatically reads the ALL_FT+ version and uses the right header for the columns provided. Versions of ALL_FT+ supported are: 2, 3, 4, 5 (same as 4), 6 and 8.

airac can be passed as a parameter to add the AIRAC to the dataframe as a column.

See main_example_read.py for an example on how to use the library (read_all_ft_functions.py). 


## Future work
- Deal with a compressed version of the ALL_FT+ automatically so that the path given to read_all_FT could be the 'raw' ALL_FT+ or a zipped version. This is important as ALL_FT+ files can be very large, and their compressed version is much smaller.

- Provide a function to automatically read all ALL_FT+ from a given folder.


## Licence
The library is released under the GPL v3 licence. The licence can be found in LICENCE.TXT