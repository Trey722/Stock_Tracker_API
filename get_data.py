import yfinance as yf
import json
import pandas as pd
import convert



def create_ticker_object(tickerSymbol):
    try:
        return yf.Ticker(tickerSymbol)
    except:
        raise TypeError("Failed to convert to ticker type")


def get_stock_price(ticker_symbol):
    try:
        # Create a Ticker object for the specified stock symbol
        ticker = yf.Ticker(ticker_symbol)

        # Get historical market data for the current day
        stock_data = ticker.history(period="1d")

        # Extract the current price from the fetched data
        current_price = stock_data['Close'][0]

        return current_price
    except Exception as e:
        return f"Error fetching data: {e}"
    
    



    
    

def get_options_chain(ticker_symbol: str, date: str, option_type=None):
    try:
        ticker_object = create_ticker_object(ticker_symbol)  # Assuming create_ticker_object is defined
        options_chain = ticker_object.option_chain(date)
        
        return convert.convert_optoin_chain_to_json(options_chain)
    except Exception as e:
        return {"status": 500, "error": f"Error fetching data: {e}"}
    
    

    
def get_balanace_sheet(ticker_symbol : str):
    
    try:
        ticker_object =  create_ticker_object(ticker_symbol)
        
        balance_sheet = ticker_object.balance_sheet
        

        
        jsonData = convert.convert_pandas_json(balance_sheet)
        
      
        
        return jsonData
        
        
    except Exception as e:
        return {"status": 500, "error": f"Error fetching data: {e}"}
    

    
    

    
    
