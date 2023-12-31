import yfinance as yf



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
    