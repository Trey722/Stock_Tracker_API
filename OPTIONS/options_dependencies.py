import GENERAL.check_type
import STOCKS.stock_data_dependencies
import math
import pandas as pd
from datetime import datetime
        
def get_option_data(option_string : str):
    option_data = {}
    ticker = ""
    i = 0 
    while GENERAL.check_type.check_number(option_string[i]) == False:
        ticker += option_string[i]
        i += 1 
        
    option_data['ticker'] = ticker 
    option_data['experiation_date'] = '20' + option_string[i:i+6]
    option_data['type'] = option_string[i+6]
    option_data['strike'] = float(option_string[i+7:]) / 1000
    return  option_data


def convert_to_date(date) -> str:
    date = str(date)
    year = date[0:4]
    month = date[4:6]
    day = date[6:]
    return str(year) + "-" + str(month) + "-"+ str(day)

def get_option(ticker : str, strike : int, date : str):
    ticker_object = STOCKS.stock_data_dependencies.create_ticker_object(ticker)
    date = convert_to_date(date)
    chain = ticker_object.option_chain(date)[0]
    chain_df = pd.DataFrame(chain)
    target = chain_df.loc[chain_df['strike'] == strike]
    return target


def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate the price of a European call or put option using the Black-Scholes formula.
    
    S: Current price of the underlying asset
    K: Strike price of the option
    T: Time to expiration (in years)
    r: Risk-free interest rate
    sigma: Volatility of the underlying asset
    option_type: 'call' for call option (default), 'put' for put option
    
    Returns the option price.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'C':
        option_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    elif option_type == 'P':
        option_price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    return option_price

def norm_cdf(x):
    """Calculate the cumulative distribution function of the standard normal distribution."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    
        
def delta_time(date1, date2):
    date1 = convert_to_date(date1)
    date2 = convert_to_date(date2)
    date1_dt = datetime.strptime(date1, "%Y-%m-%d")
    date2_dt = datetime.strptime(date2, "%Y-%m-%d")
    
    difference = date2_dt - date1_dt
    
    return (difference.days / 365)
