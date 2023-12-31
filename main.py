from fastapi import FastAPI
import getPrice

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stock_price/{ticker}")
async def getPriceStock(ticker: str):
    try:
        price = getPrice.get_stock_price(ticker)
        if isinstance(price, float):
            return {ticker: price}
        else:
            return {"error": f"Failed to fetch price for {ticker}"}
    except Exception as e:
        return {"error": str(e)}