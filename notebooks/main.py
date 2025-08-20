import config
from data_pull import bls_series_pull
from id_validation import id_check




startYr = '2015'
endYr = '2020'
series_ids = ['LNS11300000']
bls_key = config.bls_key


def main():

    # Validate that series_ids have data 

    id_check(series_ids)

    # Access BLS API to pull requested series_ids

    data_file = bls_series_pull(series_ids, startYr, endYr, bls_key)
    
    # Print head of data files
    print(data_file.head())


if __name__ == "__main__":
    main()
