import requests
import pandas as pd
import get_api_keys


fred_api_key = get_api_keys.get_fed_api_key()

def request_fred(api_key, series_id):
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError(f"Failed to fetch data. Status code: {response.status_code}")

def get_last_observation(api_key, series_id):
    try:
        data = request_fred(api_key, series_id)
        df_data = pd.DataFrame(data['observations'])
        last_observation = df_data.iloc[[-1]]
        return last_observation
    except Exception as e:
        return f"Error: {e}"
    
    

   



    