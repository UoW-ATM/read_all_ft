import argparse

from read_all_ft_functions import read_all_ft, format_all_ft


def main():
    parser = argparse.ArgumentParser(description='Example of reading a ALL_FT+ file and creating a pandas dataframe',
                                                 add_help=True)
    parser.add_argument('-f', '--file', help='path to the ALL_FT+ file', required=True)
    parser.add_argument('-a', '--airac', help='AIRAC of ALL_FT+ file', required=False)

    args = parser.parse_args()

    if args.airac is not None:
        print("Reading file", args.file, args.airac)
        airac = int(args.airac)
    else:
        print("Reading file", args.file)
        airac = None

    # Reading the ALL_FT+ file
    df, ddr_version = read_all_ft(args.file, airac)

    print("ALL_FT+ version:", ddr_version)
    print("ORIGINAL ALL_FT+")
    print(df.head())

    # Formatting columns of ALL_FT+ (optional but to transform str datetime columns in right str format, for example)
    df_formatted = format_all_ft(df, ddr_version)
    print("FORMATTED")
    print(df_formatted.head())


if __name__ == "__main__":
    # Example of use  python3 ./main_example_read.py -f ./20190901.ALL_FT+
    main()
