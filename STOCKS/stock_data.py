import yfinance as yf
import json
import pandas as pd
from STOCKS import stock_data_dependencies


def get_stock_price(ticker_symbol):
    try:
        # Create a Ticker object for the specified stock symbol
        ticker = yf.Ticker(ticker_symbol)

        # Get historical market data for the current day
        stock_data = ticker.history(period="1d")

        # Extract the current price from the fetched data
        current_price = stock_data['Close'].iloc[0]

        return current_price
    except Exception as e:
        return f"Error fetching data: {e}"  

def get_options_chain(ticker_symbol: str, date: str, option_type=None):
    try:
        ticker_object = stock_data_dependencies.create_ticker_object(ticker_symbol)  # Assuming create_ticker_object is defined
        options_chain = ticker_object.option_chain(date)
        
        return stock_data_dependencies.convert_optoin_chain_to_json(options_chain)
    except Exception as e:
        return {"status": 500, "error": f"Error fetching data: {e}"}
    
    

    
def get_balanace_sheet(ticker_symbol : str):
    
    try:
        ticker_object =  stock_data_dependencies.create_ticker_object(ticker_symbol)
        
        balance_sheet = ticker_object.balance_sheet
        

        
        jsonData = stock_data_dependencies.convert_pandas_json(balance_sheet)
        
      
        
        return jsonData
        
        
    except Exception as e:
        return {"status": 500, "error": f"Error fetching data: {e}"}
    
    
def get_dividends_recent(ticker_symbol: str):
    try:
        # Create a ticker object for the provided ticker_symbol
        ticker_object = stock_data_dependencies.create_ticker_object(ticker_symbol)
        
        # Get dividend data for the ticker object
        dividends = ticker_object.dividends
        
        dividends_df = pd.DataFrame(dividends)
        
       
        # Convert the most recent dividend data to JSON
        return float((dividends_df.iloc[-1]).iloc[0])
        
        
    except Exception as e:
        # Return an error message if an exception occurs
        return {"status": 500, "error": f"Error fetching data: {e}"}

    
    

    
    

    
    
