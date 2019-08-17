# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:23:43 2019

@author: Drew
"""

# Import the necessary packages and data
from datetime import datetime
import numpy as np
import os
import pandas as pd

path = os.path.expanduser('~/Projects/capstone-two/data/raw/Harbor_Water_Quality.csv')
df = pd.read_csv(path, parse_dates=['Sample Date', 'Sample Time'])



# Drop all stations not present in HS_Stations_2016.pdf
survey_stations = ['K1', 'K2', 'K3', 'K4', 'K5', 'K5A', 'K6',
                  'N1', 'N3B', 'N4', 'N5', 'N6', 'G2', 'N7', 'N8',
                  'N9', 'N16', 'NR1', 'E2', 'E4', 'E6', 'E7', 'E8',
                  'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'J1', 
                  'J2', 'J3', 'J5', 'J7', 'J8', 'J9A', 'J10', 'J11',
                  'J12', 'JA1', 'N9A', 'H3', 'J14', 'J16', 'AC1',
                  'AC1', 'AC2', 'BB2', 'BB4', 'BR1', 'BR3', 'BR5',
                  'CIC2', 'CIC3', 'F1', 'F5', 'FB1', 'FLC1', 'FLC2',
                  'GB1', 'GC3', 'GC4', 'GC5', 'GC6', 'HC1', 'HC2', 
                  'HC3', 'HR1', 'HR2', 'HR03', 'LN1', 'NC0', 'NC1',
                  'NC2', 'NC3', 'PB2', 'PB3', 'SP1', 'SP2', 'WC1',
                  'WC2', 'WC3'
                  ]
df = df[df['Sampling Location'].isin(survey_stations)]



# Only use samples from after 2000
df = df[df['Sample Date'] >= datetime(2000, 1, 1)]
df = df.reset_index(drop=True)



# Drop columns that I don't need
for col in df.columns:
    if 'Oakwood' in col:
        df = df.drop(columns=col)
    elif len(df[df[col].notnull()]) < 10000:
        df = df.drop(columns=col)
        
df = df.drop(['Current Direction (Current Direction)', 
              'Wind Direction (Wind Direction)',
              'Current Speed (knot)', 'Wind Speed (mph)', 
              'Sea State ', 'Type',
              'Enterococcus Top Sample Less Than or Greater Than Result'
              ], 
              axis=1
            )



# Fix 'Weather Condition' column
df['Weather Condition (Dry or Wet)'].unique()
df = df.replace(['Dry', 'Wet'], ['D', 'W'])



# Check which columns are numeric and create a list of object columns
obj_cols = []
ok_obj_cols = ['Sampling Location', 'Sample Date', 'Sample Time', 
               'Weather Condition (Dry or Wet)'
               ]
               
for col in df:
    if col not in ok_obj_cols:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            obj_cols.append(col)

# Fix Bottom TSS
df['Bottom Total Suspended Solid (mg/L)'] \
    = df['Bottom Total Suspended Solid (mg/L)'].replace('.', np.nan)

# Fix Secchi Disk
df['Secchi Depth (ft)'] = df['Secchi Depth (ft)'].replace('3..5', '3.5')
      
# Fix Bottom PH
df['Bottom PH'] = df['Bottom PH'].replace('N', np.nan)

# Fix Top Active Chlorophyl
df['Top Active Chlorophyll \'A\' (µg/L)'] \
    = df['Top Active Chlorophyll \'A\' (µg/L)'].replace('.', np.nan)

# Fix some of total phos
df['Total Phosphorus(mg/L)'] \
    = df['Total Phosphorus(mg/L)'].replace(['0..454', '0,968'],
                                           ['0.454', '0.968'])

# Fix Top Ortho
df['Top Ortho-Phosphorus (mg/L)'] \
    = df['Top Ortho-Phosphorus (mg/L)'].replace('.', np.nan)

# Preprocess Top Fecal Col
df['Top Fecal Coliform Bacteria (Cells/100mL)'] \
    = df['Top Fecal Coliform Bacteria (Cells/100mL)'].replace('TNTC', np.nan)

# Fix bacteria
def fix_commas(string):
    '''Removes commas from strings representing numbers
    with values in the thousands'''
    try:
        string = pd.to_numeric(string)
    except:
        string = string.replace(',', '')
    return string

bacteria = ['Top Fecal Coliform Bacteria (Cells/100mL)',
           'Top Enterococci Bacteria (Cells/100mL)']

for col in bacteria:
    try:
        df[col] = df[col].apply(fix_commas)
        df[col] = pd.to_numeric(df[col])
    except:
        pass



# fix columns with '<' values
def drop_less(string):
    '''Removes commas from strings representing numbers
    with values in the thousands'''
    try:
        string = pd.to_numeric(string)
    except:
        string = pd.to_numeric(string.replace('<', ''))
    return string

less_than_cols = ['Top Nitrate/Nitrite (mg/L)', 'Top Ammonium (mg/L)',
                 'Top Ortho-Phosphorus (mg/L)', 'Top Silica (mg/L)',
                  'Total Phosphorus(mg/L)' 
                 ]

for col in less_than_cols:
    try:
        df[col] = df[col].apply(drop_less)
        df[col] = pd.to_numeric(df[col])
    except:
        pass

# Fix Latitude and Longitude errors
# Replace non-numeric Longitudes
for i in df['Long']:
    try:
        pd.to_numeric(i)
    except:
        df['Long'] = df['Long'].replace(i, np.nan)
        
# Fix Latitude and Longitude mistakes
for i, lat in enumerate(df['Lat']):
    try:
        pd.to_numeric(lat)
    except:
        lat_long = lat.split(',')
        if len(lat_long) == 2:
            df.at[i, 'Lat'] = lat_long[0]
            if len(lat_long[1]) > 1:
                df.at[i, 'Long'] = lat_long[1]


def col_strip(string):
    '''Strips strings of trailing spaces and returns
    stripped string or numeric value'''
    if type(string) == str:
        string = string.replace(' ', '')
    return string

for col in df:
    if col != 'Sample Date':
        try:
            df[col] = df[col].apply(col_strip)
            df[col] = pd.to_numeric(df[col])
        except:
            print(col)

# A couple lat and long values were swapped
for i, long in enumerate(df['Long']):
    if long > 0:
        lat = long
        long = df.iloc[i]['Lat']
        df.at[i, 'Lat'] = lat
        df.at[i, 'Long'] = long
        print(df.iloc[i].loc[['Lat', 'Long']])


# Save df to csv file
outpath = os.path.expanduser(
    '~/Projects/capstone-two/data/processed/Clean_Harbor_Water_Quality.csv'
    )

df.to_csv(outpath)