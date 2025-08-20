import config
from data_pull import bls_series_pull
from data_export import export_to_excel
from id_validation import id_check
import os
import pandas as pd




startYr = int('2015')
endYr = int('2020')
series_ids = ['LNS11300000']
bls_key = config.bls_key


def main():

    # Validate that series_ids have data 

    id_check(series_ids, startYr, endYr, bls_key)

    # Access BLS API to pull requested series_ids

    data_file = bls_series_pull(series_ids, startYr, endYr, bls_key)
    
    # Convert data file to csv and save in data folder
    export_to_excel(data_file)

    # Print head of data files
    print(data_file.head())


if __name__ == "__main__":
    main()
