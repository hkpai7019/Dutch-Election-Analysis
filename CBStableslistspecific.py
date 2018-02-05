import cbsodata
import pandas as pd
import re
import numpy as np
import math


def test_for_regios(identifier, output_df=gemeente_tables_info):
    ''' Function to check whether the table has a regios/regions column

    Args:
        identifier: enter an identifier for a particular table with quotation, e.g., '37201'
        output_df: DataFrame to add information to. Default is gemeente_tables_info

    Returns:
        updated dataframe gemeente_tables_info with the information of whether the table in that
        row has a regios/regions column.
    '''
    # Import data into data_df
    data_df = pd.DataFrame(cbsodata.get_data(identifier))

    # Make the column names all in lower case, in case there are different formats.
    data_df.columns = [x.lower() for x in data_df.columns]

    # Populate regios column
    if {'regios'}.issubset(data_df.columns) == True:
        output_df.loc[output_df['identifier'] == identifier, 'regios'] = 1
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'regios'] is not np.nan, 'Assignment of regios identifier failed, regios column present'
        print('Regions columns populated for {}'.format(identifier))
        return output_df

    elif {'regions'}.issubset(data_df.columns) == True:
        output_df.loc[output_df['identifier'] == identifier, 'regios'] = 1
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'regios'] is not np.nan, 'Assignment of regios identifier failed, regios column present'
        print('Regios columns populated for {}'.format(identifier))
        return output_df

    else:
        print("This table does not contain regios as a column.")
        output_df.loc[output_df['identifier'] == identifier, 'regios'] = 0
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'regios'] is not np.nan, 'Assignment of regios identifier failed, regios column present'
        print('Regios columns populated for {}'.format(identifier))
        return output_df


def test_for_perioden(identifier, output_df=gemeente_tables_info):
    ''' Function to check whether the table has a perioden/period column

    Args:
        identifier: enter an identifier for a particular table with quotation, e.g., '37201'
        output_df: DataFrame to add information to. Default is gemeente_tables_info

    Returns:
        updated dataframe gemeente_tables_info with the information of whether the table in that
        row has a perioden/period column.
    '''
    data_df = pd.DataFrame(cbsodata.get_data(identifier))

    # Make the column names all in lower case, in case there are different formats.
    data_df.columns = [x.lower() for x in data_df.columns]

    # Populate perioden column
    if {'perioden'}.issubset(data_df.columns) == True:
        output_df.loc[output_df['identifier'] == identifier, 'perioden'] = 1
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'perioden'] is not np.nan, 'Assignment of Perioden identifier failed, Perioden column present'
        print('Perioden columns populated for {}'.format(identifier))
        return output_df

    elif {'periods'}.issubset(data_df.columns) == True:
        output_df.loc[output_df['identifier'] == identifier, 'perioden'] = 1
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'perioden'] is not np.nan, 'Assignment of Perioden identifier failed, Perioden column present'
        print('Perioden columns populated for {}'.format(identifier))
        return output_df

    else:
        print("This table does not contain perioden as a column.")
        output_df.loc[output_df['identifier'] == identifier, 'perioden'] = 0
        assert output_df.loc[output_df[
                                 'identifier'] == identifier, 'perioden'] is not np.nan, 'Assignment of Perioden identifier failed, Perioden column present'
        print('Perioden columns populated for {}'.format(identifier))
        return output_df


def test_for_gemeente_desc(identifier, output_df=gemeente_tables_info):
    ''' Function to check whether the table mentioned "gemeente" in its ShortDescription column

    Args:
        identifier: enter an identifier for a particular table with quotation, e.g., '37201'
        output_df: DataFrame to add information to. Default is gemeente_tables_info

    Returns:
        updated dataframe gemeente_tables_info with the information of whether the table in that
        row actually mentioned "gemeente" in its ShortDescription column.
    '''

    tables_gemeente = tables[tables['ShortDescription'].str.contains('gemeente')]
    tables_gemeente.columns = [x.lower() for x in tables_gemeente.columns]

    tables_gemeente2 = tables[tables['ShortDescription'].str.contains('municipal')]
    tables_gemeente2.columns = [x.lower() for x in tables_gemeente2.columns]

    if (tables_gemeente['identifier'].astype(str).str.contains(identifier)).any() == True:
        output_df.loc[output_df['identifier'] == identifier, 'gemeente'] = 1
        print('Gemeente in ShortDescription column for {}, gemeente column set to yes'.format(identifier))
        return output_df
    elif (tables_gemeente2['identifier'].astype(str).str.contains(identifier)).any() == True:
        output_df.loc[output_df['identifier'] == identifier, 'gemeente'] = 1
        print('Gemeente in ShortDescription column for {}, gemeente column set to yes'.format(identifier))
        return output_df

    else:
        print('This table does not mention gemeente in its ShortDescription column')
        output_df.loc[output_df['identifier'] == identifier, 'gemeente'] = 0
        return output_df
