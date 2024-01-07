from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
import json


import STOCKS.stock_data
import STOCKS.margin_calcualtor


import FRED.get_fred_data
import OPTIONS.calc_options
import OPTIONS.option_object
import OPTIONS.hedging




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
        options_data = STOCKS.stock_data.get_options_chain(ticker, date)
        return options_data
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
        if starting_price > ending_price:
            raise TypeError("Starting Price can't be greater then endingprice")
        elif (step <= 0):
            raise TypeError("Step needs to be greater then 0")
            
        starting_price = float(starting_price)
        ending_price = float(ending_price)
        step = float(step)
        return json.dumps(OPTIONS.calc_options.calculate_profit(starting_price, ending_price, step, ticker, False))
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
@app.get("/CALC/STOCKS/PROFIT/{quantity}/{underlying_stock_price}/{margin_used}/{starting_price}/{ending_price}/{step}")
async def calc_stock_profit(quantity, underlying_stock_price, margin_used, starting_price, ending_price, step):
    try:
        starting_price = float(starting_price)
        ending_price = float(ending_price)
        margin_used = float(margin_used)
        underlying_stock_price = float(underlying_stock_price)
        step = float(step)
        
        if starting_price > ending_price:
            raise ValueError("Starting Price can't be greater than ending price")
        elif step <= 0:
            raise ValueError("Step needs to be greater than 0")
        
        quantity = int(quantity)
        
        # Call your function to calculate stock profits here
        result = STOCKS.margin_calcualtor.calculate_margin(quantity, underlying_stock_price, margin_used, starting_price, ending_price, step)
        
        return {"result": result}
    except Exception as e:
         return {"status": 500, "error": str(e)}
    
    
@app.get("/CALC/OPTION/HEDGE/DELTA/Gamma/{quantity}/{delta_option1}/{gamma_option1}/{delta_option2}/{gamma_option2}")
async def CALC_gamma_hegde(quantity, delta_option1, gamma_option1, delta_option2, gamma_option2):
    try:
        quantity = int(quantity)
        delta_option1 = float(delta_option1)
        gamma_option1 = float(gamma_option1)
        delta_option2 = float(delta_option2)
        gamma_option2 = float(gamma_option2)
        print(delta_option1, gamma_option1, delta_option2, gamma_option2)
        print(OPTIONS.hedging.gamma_hedge_simple(quantity, delta_option1, gamma_option1, delta_option2, gamma_option2))
        return json.dumps(OPTIONS.hedging.gamma_hedge_simple(quantity, delta_option1, gamma_option1, delta_option2, gamma_option2))
    except Exception as e:
        return {"status": 500, "error": str(e)}
        
    
    

    
    