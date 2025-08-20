import json
import requests
import pandas as pd

def id_check(industry_list, bls_key, startYr='2015', endYr='2020', verbose=True):
        
    """
    Validate which BLS series IDs return data, with industry names included.
    
    Parameters
    ----------
    industry_list : list of [seriesID, industry_name]
        List of series IDs with their industry names.
    bls_key : str
        Your BLS API key.
    startYr : str, optional
        Start year for test query (default "2020").
    endYr : str, optional
        End year for test query (default "2020").
    verbose : bool, optional
        Print results as validation runs.
    
    Returns
    -------
    results_df : pd.DataFrame
        DataFrame with columns: [seriesID, industry_name, status, n_rows, message]
    """
# Testing ids to ensure they return data

    results = []
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data"
    headers = {"Content-type": "application/json"}

    for sid in industry_list:
        payload = json.dumps({
            "seriesid": [sid],
            "startyear": startYr,
            "endyear": endYr,
            "registrationKey": bls_key
        })

        status = "invalid"
        n_rows = 0
        message = ""

        try:
            r = requests.post(url, data=payload, headers=headers, timeout=10)
            r.raise_for_status()
            json_data = r.json()

            if "Results" in json_data and "series" in json_data["Results"]:
                series_data = json_data["Results"]["series"][0]["data"]
                n_rows = len(series_data)
                if n_rows > 0:
                    status = "valid"
                    message = "Returned rows"
                    if verbose:
                        print(f"✅ {sid} ({industry_list}) returned {n_rows} rows")
                else:
                    status = "empty"
                    message = "No data returned"
                    if verbose:
                        print(f"⚠️ {sid} ({industry_list}) returned no data")
            else:
                status = "invalid"
                message = str(json_data.get("message", "Invalid response"))
                if verbose:
                    print(f"❌ {sid} ({industry_list}) invalid response: {message}")

        except Exception as e:
            status = "error"
            message = str(e)
            if verbose:
                print(f"❌ {sid} ({industry_list}) error: {e}")

        results.append([sid, industry_list, status, n_rows, message])

    results_df = pd.DataFrame(results, columns=["seriesID", "industry_name", "status", "n_rows", "message"])
    return results_df