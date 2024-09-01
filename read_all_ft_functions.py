import pandas as pd
import ddr_headers as ddrh

__version__ = 6.0


# READ ALL_FT+ FILES

def read_all_ft(allft_path, airac=None):
    # READ FILE WITH TRAFFIC DATA AND CREATE PANDA STRUCTURE WITH HEADER OF DDR
    data = pd.read_csv(allft_path, sep=";", skiprows=1, header=None)
    
    lpos = max(allft_path.rfind('\\'), allft_path.rfind('/'))
    ddr_source = allft_path[lpos+1:]

    # with open(allft_path) as f:
    #    ddr_version = int(f.readline())
    ddr_version_dat = pd.read_csv(allft_path, nrows=1, header=None)
    ddr_version = ddr_version_dat.iloc[0, 0]
    
    h_ddrv2, h_ddrv3, h_ddrv4, h_ddrv6, h_ddrv8 = ddrh.ddr_headers()

    # print(ddr_version)

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


def format_all_ft(data, ddr_version):

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
