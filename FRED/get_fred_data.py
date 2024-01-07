import FRED.fred_data_dependencies
from FRED.fred_data_dependencies import fred_api_key


def get_risk_free_intrest_rate():
    series_id = 'DGS10'
    row = float(FRED.fred_data_dependencies.get_last_observation(fred_api_key, series_id)['value'].iloc[0])
    return row


def get_gdp(year):
    # FRED series ID for Real Gross Domestic Product (GDPC1)
    series_id = 'GDPC1'
    

    
    data = FRED.fred_data_dependencies.request_fred(fred_api_key, series_id)
    observations = data['observations']
    
    return data


    
