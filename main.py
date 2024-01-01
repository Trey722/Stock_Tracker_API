from fastapi import FastAPI
import get_stock_data
from pydantic import BaseModel, Field

from starlette.middleware.cors import CORSMiddleware



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
        price = get_stock_data.get_stock_price(ticker)
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
        options_data = get_stock_data.get_options_chain(ticker, date)
        return options_data
    except Exception as e:
        return {"status": 500, "error": str(e)}
    
    
@app.get("/stock/data/balanace_sheet/{ticker}")
async def get_balanace_sheet_endpoint(ticker):
    try:
        return get_stock_data.get_balanace_sheet(ticker)
    except Exception as e:
        return {"status": 500, "error": str(e)}

        
        

    
    
