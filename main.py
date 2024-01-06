from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
import json


import STOCKS.stock_data
import FRED.get_fred_data
import OPTIONS.calc_options
import OPTIONS.option_object




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origins here (e.g., ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/stock/data/stock_price/{ticker}")
async def getPriceStock(ticker: str):
    try:
        price = STOCKS.stock_data.get_stock_price(ticker)
        if isinstance(price, float):
            return {ticker: price}
        else:
            return {"status": 502,"error": f"Failed to fetch price for {ticker}"}
    except Exception as e:
        return {"status": 500,"error": str(e)}
    
    
    
@app.get("/stock/data/options_chain/{ticker}/{date}")
async def get_options_chain_endpoint(ticker: str, date):
    try:
        date = str(date)
        options_data = STOCKS.stock_data.get_stock_data.get_options_chain(ticker, date)
        return options_data
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
    
@app.get("/stock/data/balanace_sheet/{ticker}")
async def get_balanace_sheet_endpoint(ticker):
    try:
        return STOCKS.stock_data.get_balanace_sheet(ticker)
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
@app.get("/ECON/DATA/risk_free_rate")
async def get_risk_free_rate():
    try:
        return FRED.get_fred_data.get_risk_free_intrest_rate()
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
    
    
@app.get("/OPTIONS/DATA/{ticker}/Greeks")
async def get_ticker(ticker):
    try:
        
       return json.dumps(OPTIONS.option_object.option_object(ticker).get_greeks())
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
@app.get("/CALC/OPTION/BUYING/{starting_price}/{ending_price}/{step}/{ticker}")
async def CALC_option_value(starting_price, ending_price, step, ticker):
       try:
           starting_price = float(starting_price)
           ending_price = float(ending_price)
           step = float(step)
           return json.dumps(OPTIONS.calc_options.calculate_profit(starting_price, ending_price, step, ticker))
       except Exception as e:
           return {"status": 500, "error": str(e)}
       
       
@app.get("/CALC/OPTION/SELLING/{starting_price}/{ending_price}/{step}/{ticker}")
async def CALC_option_value_selling(starting_price, ending_price, step, ticker):
    try:
        starting_price = float(starting_price)
        ending_price = float(ending_price)
        step = float(step)
        return json.dumps(OPTIONS.calc_options.calculate_profit(starting_price, ending_price, step, ticker, False))
    except Exception as e:
        return {"status": 500, "error": str(e)}

    
    