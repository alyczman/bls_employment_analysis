import pandas as pd
import requests
import json
import config

def main(seriesID, StartYr, EndYr, bls_key):
    headers = {'Content-type':'application/json'}
    # api url
    bls_api_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data'

    # setup inputs to the API: series ID, start year, end year, and api key

    data = json.dumps({'SeriesID': [seriesID], 
                       'startyear': StartYr, 
                       'endyear': EndYr, 
                       'registrationKey':bls_key})

    # access the api and extract the outputs
    p = requests.post(bls_api_url, data=data, 
                      headers=headers)
    json_data = p.json()

    # parse the output into the list
    series_data = []
    try:
        for series in json_data['Results']['Series']:
            seriesID = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']

        if 'M01' <= period <= 'M12':
            series_data.append([seriesID, year, period, value])
    except KeyError as e:
        print('Error in API response:', json_data)
        raise e
    
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

    # Convert industry list into data frame
    industries_df = pd.DataFrame(Industry_list, columns=["seriesID", "Industry_name"])
    print('Industry reference table: ')
    print(industries_df.head(), "\n")


    # Setup parameters
    StartYr = '2015'
    EndYr = '2020'# Set your BLS API Key here
    key = config.bls_key #Setup Schema of the data sent from BLS

    # Create list to capture the data
    complete_list = []


    # Loop through the series IDs and gather the data into a list object
        
    for id in industries_df["seriesID"]:
        print(f'Fetching data for {id}...')
        complete_list.extend(main(id, 
                                StartYr,
                                EndYr,
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

