import cbsodata
import pandas as pd
import re
import numpy as np
import math

def generate_gemeente_tables_info(tables):
    ''' Function that selects tables from the raw data of all tables from CBS and adds columns

    Args:
        tables: (df) A dataframe with raw CBS table of all data tables they have

    Returns:
        A dataframe with:
                            identifier: a code that uniquely identifies each table
                            period: a column that has the years the table was kept
                            frequency: the update freqency of the table (if still updated, else 'stopgezet')
                            title: the title of the table (in Dutch)
                            shortdescription: table description (in Dutch)

                            regios: a column that will be populated with geographical identifier
                            perioden: will be populated with years active
                            gemeente: will be populated with years below
    '''

    gemeente_tables_info = tables[['Identifier', 'Period', 'Frequency', 'Title', 'ShortDescription']].copy()
    gemeente_tables_info['regios'] = np.nan
    gemeente_tables_info['perioden'] = np.nan
    gemeente_tables_info['gemeente'] = np.nan
    gemeente_tables_info.columns = [x.lower() for x in gemeente_tables_info.columns]

    return gemeente_tables_info


def get_start_end_year(df, column='period'):
    ''' Function to return start and end year to dataframe

    Args:
        df:  A with tables from generate_gemeente_tables_info
        column: A column within the dataframe that identifies the time active for each table

    Returns:
        df with two new columns, 'start_year' and 'end_year', in pd.datetime format
    '''

    # check if input is dataframe, and column is str
    if not isinstance(df, pd.DataFrame):
        raise TypeError('input should be DataFrame, got {} instead'.format(type(df)))
    if not isinstance(column, str):
        raise TypeError('input should be string, got {} instead'.format(type(column)))

    # Start by extracting the years from column, return as string
    df['matches'] = df[column].str.findall('\d{4}')

    # create new columns
    df['start_year'] = df['matches'].apply(lambda x: min(x) if x else np.nan)
    df['start_year'] = pd.to_datetime(df['start_year'], format=('%Y'))
    df['end_year'] = df['matches'].apply(lambda x: max(x) if x else np.nan)
    df['end_year'] = pd.to_datetime(df['end_year'])

    # drop the matches column
    df.drop(['matches'], axis=1, inplace=True)

    return df


def frequency_coder(df, column='frequency'):
    ''' Function to generate the two frequency-related columns, freq_num and freq_unit, using information from
        the original frequency column.

    Args:
        df: already preset to be gemeente_tables_info
        column: already pre-set to be 'frequency'

    Returns:
        updated dataframe gemeente_tables_info with the two new columns - freq_num and freq_unit.
    '''
    # First create the two dictionaries:
    dict_freq_num = {
        'Stopgezet': 'discontinued', 'Discontinued': 'discontinued',
        'Perjaar': 1, 'Yearly': 1,
        'Eenmalig': 1, 'Onceonly': 1,
        'Perkwartaal': 1, 'Quarterly': 1, 'Perdriemaanden': 1, 'Viermaalperjaar': 1, 'Threemonthly': 1,
        'maand': 1, 'Monthly': 1, 'Permaand': 1,
        'Onregelmatig': 'irregularly', 'Irregularly': 'irregularly',
        'Tweemaalperjaar': 2, 'Perhalfjaar': 2, 'Twiceyearly': 2,
        'Driemaalperjaar': 3, 'Threetimesayear': 3,
        'Pertweejaar': 0.5, 'Twoyearly': 0.5,
        'Perdriejaar': float(1 / 3), 'Threeyearly': float(1 / 3),
        'Pervierjaar': 0.25, 'Fouryearly': 0.25,
        'Pervijfjaar': 0.2, 'Fiveyearly': 0.2,
        'Tijdelijkstopgezet': 'temporarily_suspended',
        'Twicemonthly': 2, 'Tweemaalpermaand': 2,
        'Perweek': 1,
        'Pertweeweken': 0.5
    }

    dict_freq_unit = {
        'Stopgezet': 'discontinued', 'Discontinued': 'discontinued',
        'Perjaar': 'y', 'Yearly': 'y',
        'Eenmalig': 'once', 'Onceonly': 'once',
        'Perkwartaal': 'q', 'Quarterly': 'q', 'Perdriemaanden': 'q', 'Viermaalperjaar': 'q', 'Threemonthly': 'q',
        'maand': 'm', 'Monthly': 'm', 'Permaand': 1,
        'Onregelmatig': 'irregularly', 'Irregularly': 'irregularly',
        'Tweemaalperjaar': 'y', 'Perhalfjaar': 'y', 'Twiceyearly': 'y',
        'Driemaalperjaar': 'y', 'Threetimesayear': 'y',
        'Pertweejaar': 'y', 'Twoyearly': 'y',
        'Perdriejaar': 'y', 'Threeyearly': 'y',
        'Pervierjaar': 'y', 'Fouryearly': 'y',
        'Pervijfjaar': 'y', 'Fiveyearly': 'y',
        'Tijdelijkstopgezet': 'temporarily_suspended',
        'Twicemonthly': 'm', 'Tweemaalpermaand': 'm',
        'Perweek': 'w',
        'Pertweeweken': 'w'
    }

    # Change the columns to lower-case, just in case
    df.columns = [x.lower() for x in df.columns]

    # LH: changed this to work
    if column in df.columns:
        df['freq_num'] = df[column].map(dict_freq_num)
        df['freq_unit'] = df[column].map(dict_freq_unit)
    else:
        raise ValueError('Table does not have frequency column')

    return df


