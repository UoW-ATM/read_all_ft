import pandas as pd
import re
from datetime import datetime


def convert_coordinates(coord):
    """
    Converts string formatted as "400741N0325942E" in latitude/longitude coordinates in degrees.
    """
    # Extract latitude
    lat_deg = int(coord[:2])  # Latitude degrees
    lat_min = int(coord[2:4])  # Latitude minutes
    lat_min_decimal = int(coord[4:6])  # Latitude minutes decimal
    lat = lat_deg + lat_min / 60 + lat_min_decimal / 6000

    # Check if latitude is North or South (N or S)
    if coord[6] == 'S':
        lat = -lat

    # Extract longitude
    lon_deg = int(coord[7:10])  # Longitude degrees
    lon_min = int(coord[10:12])  # Longitude minutes
    lon_min_decimal = int(coord[12:14])  # Longitude minutes decimal
    lon = lon_deg + lon_min / 60 + lon_min_decimal / 6000

    # Check if longitude is East or West (E or W)
    if coord[14] == 'W':
        lon = -lon

    return lat, lon


def extract_altitude(entry):
    """
    Extract from a string the altitude in flight level
    """
    # Regular expression to match altitude, assumed to be a number ending with 'ft' or standalone
    altitude_pattern = r'(?<=:)(\d+)(?=\:|\s|$)'
    altitude_match = re.search(altitude_pattern, entry)
    if altitude_match:
        return int(altitude_match.group(1))  # Convert altitude to integer
    return None  # Return None if no altitude found


def extract_all_trajectories(df_all_ft, traj_type='ctfm'):
    """
    Careful, this can take a while, and the results dataframe can be big
    """
    ifps_ids = list(df_all_ft['ifps_id'])

    dfs = []
    for ifps_id in ifps_ids:
        df = extract_trajectory(ifps_id, df_all_ft, traj_type=traj_type)
        if df is not None:
            df.loc[:, 'ifps_id'] = ifps_id
            dfs.append(df)
        else:
            # print('No trajectory for', ifps_id)
            pass

    return pd.concat(dfs)


def extract_trajectory(ifps_id, df_all_ft, traj_type='ctfm'):
    """
    Given a dataframe extracted via the function "read_all_ft_formatted" for instance, extract the trajectory of a given
    flight as dataframe.
    """
    try:
        assert traj_type in ['ctfm', 'ftfm']
    except AssertionError:
        raise AssertionError("'traj_type' needs to be 'ctfm' or 'ftfm'")

    field_traj = '{}AllFtPointProfile'.format(traj_type)
    matching_row = df_all_ft.loc[df_all_ft['ifps_id'] == ifps_id]

    if matching_row.empty:
        raise Exception("Couldn't find flight id", ifps_id)

    trajectory_string = matching_row[field_traj].values[0]

    # Find all matches for timestamps and coordinates
    coordinate_pattern = r'(\d{6}[NS]\d{7}[EW])'
    timestamp_pattern = r'2019\d{10}'

    if not pd.isnull(trajectory_string):
        try:
            timestamps = re.findall(timestamp_pattern, trajectory_string)
        except:
            print(trajectory_string)
            raise
        coordinates = re.findall(coordinate_pattern, trajectory_string)
        entries = trajectory_string.split()  # Split the input string into parts to process altitude

        # TODO: use apply...
        # Prepare data for DataFrame
        data = []
        # Iterate through the lists of timestamps, coordinates, and entries
        for timestamp, coord, entry in zip(timestamps, coordinates, entries):
            lat, lon = convert_coordinates(coord)
            altitude = extract_altitude(entry)
            dt_formatted = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            data.append([dt_formatted, lon, lat, altitude])

        # Create DataFrame with reordered columns
        df_trajectory = pd.DataFrame(data, columns=["Timestamp", "Longitude", "Latitude", "FL"])

        return df_trajectory


if __name__ == "__main__":
    # Testing

    import sys
    sys.path.insert(1, '..')
    from read_all_ft_functions import read_all_ft_formatted

    allft_path = "/home/earendil/Documents/Westminster/Data/DDR/archive_20240110_1142_7/20190901.ALL_FT+"
    print('Reading ALLFT+ file...')
    df_all_ft = read_all_ft_formatted(allft_path)

    ifps_id = df_all_ft.iloc[0]['ifps_id']
    print('IFPS ID:', ifps_id)

    df_trajectory = extract_trajectory(ifps_id, df_all_ft)

    print(df_trajectory)

    df_all = extract_all_trajectories(df_all_ft, traj_type='ctfm')
    print(df_all)
