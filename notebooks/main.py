from id_validation import id_check
import pandas as pd
import prettytable
import requests
import json
import config

def main(seriesID, startYr, endYr, bls_key):
    headers = {'Content-type':'application/json'}
    # api url
    bls_api_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data'

    # setup inputs to the API: series ID, start year, end year, and api key

    data = json.dumps({'seriesID': [seriesID], 
                       'startyear': startYr, 
                       'endyear': endYr, 
                       'registrationKey':bls_key})

    # access the api and extract the outputs
    p = requests.post(bls_api_url, data=data, 
                      headers=headers)
    json_data = json.loads(p.text)

    if 'Results' not in json_data:
        print(f'No results found for {seriesID}: {json_data}')
        return []
    

    # parse the output into the list
    series_data = []

    for series in json_data['Results']['series']:
        x = prettytable(['series id', 'year', 'period', 'value'])
        seriesID = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']

            if period.startswith('M') and 1 <= int(period[1:]) <= 12:
                series_data.append([seriesID, year, period, value])
    
    
    return series_data

if __name__ == "__main__":
    Industry_list = [
        ['CEU0000000001','Total nonfarm'],
        ['CEU0500000001','Total private'],
        ['CEU0600000001','Goods-producing'],
        ['CEU0700000001','Service-providing'],
        ['CEU4000000001','Trade, transportation, and utilities'],
        ['CEU4142000001','Wholesale trade'],
        ['CEU4200000001','Retail trade'],
        ['CEU6056150001','Travel arrangement and reservation services'],
        ['CEU7072250001','Restaurants and other eating places'],
        ['CEU7071000001','Arts, entertainment, and recreation'],
        ['CEU6054150001','Computer systems design and related services'],
        ['CEU6054161001','Management consulting services']
    ]

    validation_check = id_check(Industry_list, config.bls_key)

    # Convert industry list into data frame
    industries_df = pd.DataFrame(Industry_list, columns=["seriesID", "Industry_name"])
    print('Industry reference table: ')
    print(industries_df.head(), "\n")


    # Setup parameters
    startYr = '2015'
    endYr = '2020'
    key = config.bls_key # BLS Key

    # Create list to capture the data
    complete_list = []


    # Loop through the series IDs and gather the data into a list object
        
    for id in industries_df["seriesID"]:
        print(f'Fetching data for {id}...')
        complete_list.extend(main(id, 
                                startYr,
                                endYr,
                                key))


    # Convert to dataframe
    bls_df = pd.DataFrame(complete_list, columns=['seriesID',
                                                'year',
                                                'period',
                                                'value'])

    # convert datatypes
    bls_df['year'] = bls_df['year'].astype(int)
    bls_df['value'] = bls_df['value'].astype(float)

    # Create date column
    bls_df['month'] = bls_df['period'].str[1:].astype(int) #strip "M" and convert
    bls_df['date'] = pd.to_datetime(bls_df['year'].astype(str) + "-" + bls_df['month'].astype(str) +'01')

    print("\nSample of final Dataframe: ")
    print(bls_df.head())

