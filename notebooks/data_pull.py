import pandas as pd
import prettytable
import requests
import json


def bls_series_pull(seriesID, startYr, endYr, bls_key):
    headers = {'Content-type':'application/json'}
    # api url
    bls_api_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data'
   

    # setup inputs to the API: series ID, start year, end year, and api key

    data = json.dumps({'seriesid': series_ids, 
                       'startyear': startYr, 
                       'endyear': endYr, 
                       'registrationKey':bls_key})

    # access the api and extract the outputs
    p = requests.post(bls_api_url, data=data, 
                      headers=headers)
    json_data = json.loads(p.text)

    if 'Results' not in json_data:
        print(f'No results found for {seriesID}: {json_data}')
        return pd.DataFrame()
    

    # parse the output into the list
    series_data = []

    for series in json_data['Results']['series']:
        x = prettytable.PrettyTable(['series id', 'year', 'period', 'value']) # will use this in a later iterations
        seriesID = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']

            if 'M01' <= period <= 'M12':
                x.add_row([seriesID, year, period, value])

                series_data.append({'seriesID': seriesID,
                               'year': year,
                               'period':period,
                               'value': value})
    
    df = pd.DataFrame(series_data)
    return df
