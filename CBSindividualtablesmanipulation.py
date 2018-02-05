import cbsodata
import pandas as pd
import re
import numpy as np
import math


def gemeente_format(identifier):
    ''' Function to check if the specific table (note: not the table-list dataframe)
        has a regios/regions column and reformat the column (i.e. make sure it is
        in string format, all in lower-case, and all English alphabets).

    Args:
        identifier:  The identifier of a specific table

    Returns:
        A new dataframe where the regios/regions column is reformatted.
    '''
    df = pd.DataFrame(cbsodata.get_data(identifier))
    df.columns = [x.lower() for x in df.columns]

    if {'regios'}.issubset(df.columns) == True:
        df['regios'] = df['regios'].apply(lambda x: x.encode('utf-8').strip())
        df['regios'] = df['regios'].astype(str)
        df['regios'] = df['regios'].str.lower()
        df['regios'] = df['regios'].str.replace(r"[^a-zA-Z]+", r"")
        # df['regios'] = u'{}'.format(df['regios']).lower()
        return df
    elif {'regions'}.issubset(df.columns) == True:
        df['regios'] = df['regios'].apply(lambda x: x.encode('utf-8').strip())
        df['regions'] = df['regions'].astype(str)
        df['regions'] = df['regions'].str.lower()
        df['regions'] = df['regions'].str.replace(r"[^a-zA-Z]+", r"")
        # df['regions'] = u'{}'.format(df['regions']).lower()
        return df
    else:
        print("This table doesn't contain a gemeente column.")

def create_gemeente_hist(df=tables):
    ''' Function to generate a dataframe/table with gemeente's info on its code,
        begin-, and end- years.

    Args:
        df:  the "tables" dataframe. Probably shouldn't change this.

    Returns:
        gemeente_hist: a newly generated dataframe that has four columns,
        gemeente, gemeente_code, begin_year, and end_year
    '''
    gemeente_hist_id =tables[df['Title' ]=='Gebieden; overzicht vanaf 1830']['Identifier'].item()
    gemeente_hist0 = pd.DataFrame(cbsodata.get_data(gemeente_hist_id))

    gemeente_hist0['begin_year'] = gemeente_hist0['Begindatum_1'].str.findall('\d{4}')
    gemeente_hist0['begin_year'] = [list(map(float, x)) for x in gemeente_hist0['begin_year']]
    gemeente_hist0['begin_year'] = gemeente_hist0['begin_year'].apply(lambda x: min(x) if x else np.nan)

    gemeente_hist0['end_year'] = gemeente_hist0['Einddatum_2'].str.findall('\d{4}')
    gemeente_hist0['end_year'] = [list(map(float, x)) for x in gemeente_hist0['end_year']]
    gemeente_hist0['end_year'] = gemeente_hist0['end_year'].apply(lambda x: max(x) if x else np.nan)

    gemeente_hist = gemeente_hist0[['RegioS' ,'GebiedsOfGemeentecode_3' ,'begin_year' ,'end_year']].copy()
    gemeente_hist = gemeente_hist.rename(columns={'RegioS': 'gemeente', 'GebiedsOfGemeentecode_3': 'gemeente_code'})
    gemeente_hist.columns = [x.lower() for x in gemeente_hist.columns]

    return gemeente_hist

def keep_gemeente_columns(identifier):
    ''' Function to check whether the specific table has a regios/regions column and drop all the rows
            that are not at the gemeente-level.

    Args:
        identifier: enter an identifier for a particular table with quotation, e.g., '71356ned'

    Returns:
        updated dataframe output_df with only the gemeente-level data.
    '''
    gemeente_hist = create_gemeente_hist()
    gemeente_hist['gm'] = gemeente_hist.gemeente_code.str.slice(0, 2)
    gemeente_hist = gemeente_hist[(gemeente_hist['gm'] == 'GM') & (gemeente_hist['gemeente'] != 'Buitenland') & (
                gemeente_hist['gemeente'] != 'Niet-gemeentelijk ingedeeld')]
    gemeente_list = gemeente_hist['gemeente'].tolist()

    output_df = pd.DataFrame(cbsodata.get_data(identifier))
    output_df.columns = [x.lower() for x in output_df.columns]

    if {'regios'}.issubset(output_df.columns) == True:
        output_df = output_df[output_df['regios'].isin(gemeente_list)]
        output_df = output_df.reset_index()
        return output_df

    elif {'regions'}.issubset(output_df.columns) == True:
        output_df = output_df[output_df['regions'].isin(gemeente_list)]
        output_df = output_df.reset_index()
        return output_df

    else:
        print("This table does not contain regios as a column.")


dict_geocode = {
    'LD': 'Landsdeel', 'PV': 'Provincie',
    'SG': 'Stadsgewest', 'CR': 'COROP-gebied',
    'CP': 'COROP-plusgebied', 'CS': 'COROP-subgebied',
    'EG': 'Economisch Geografische Gebieden', 'GA': 'Grootstedelijke agglomeratie',
    'GM': 'Gemeente', 'KD': 'Kiesdistricten',
    'KM': 'Tweede Kamerindeling', 'BR': 'Brandweerregio',
    'LB': 'Landbouwgebied', 'LG': 'Landbouwgroep',
    'NO': 'Nodale gebieden', 'RB': 'Rayon Bureau Arbeidsvoorziening',
    'RP': 'RPA-gebied', 'PO': 'Politieregio',
    'TR': 'Toeristengebied'
}


def get_gemeentes_in_year(gemeente_hist, year):
    '''Function that accepts a year and returns a dataframe with gemeentes existing in year

    Args:
        gemeente_hist: (df) a dataframe of gemeentes and their start and end year
        yr: (float) a year

    '''

    gemeente_hist['gm'] = gemeente_hist.gemeente_code.str.slice(0, 2)
    gemeente_hist = gemeente_hist[(gemeente_hist['gm'] == 'GM') &
                                  (gemeente_hist['gemeente'] != 'Buitenland') &
                                  (gemeente_hist['gemeente'] != 'Niet-gemeentelijk ingedeeld')]

    return (gemeente_hist[
        (gemeente_hist.begin_year <= year) & ((gemeente_hist.end_year >= year) | (gemeente_hist.end_year.isnull()))])


def generate_gemeente_in_each_year_dict(gemeente_hist=create_gemeente_hist(), start_year=1950, end_year=2017):
    '''Function that generates a dict that has the gemeentes that were extant in each year

    Args:
        gemeente_hist: (df) dataframe with for each gemeente it's start and end year; note create_gemeente_hist function
                        is needed
        start_year: (int) start year of dict
        end_year: (int) end year of dict

    Returns:
        A dict with years as keys and a df for each year
    '''

    dict_gemeente_by_year = {}

    for i in range(start_year, end_year):
        dict_gemeente_by_year[i] = get_gemeentes_in_year(gemeente_hist, i)

    return dict_gemeente_by_year

