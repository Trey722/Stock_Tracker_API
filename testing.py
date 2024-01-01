import yfinance as yf

def get_stocks_in_fund(fund_symbol):
    try:
        fund = yf.Ticker(fund_symbol)
        holdings = fund.get_holdings()  # Retrieves holdings information
        # Extract stocks from holdings data
        stocks = holdings['symbol'].tolist() if 'symbol' in holdings else None
        return stocks
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
fund_symbol = 'ARKK'  # Replace with the symbol of the fund you want to explore
stocks_in_fund = get_stocks_in_fund(fund_symbol)
if stocks_in_fund:
    print(f"Stocks within {fund_symbol}: {stocks_in_fund}")
else:
    print("Failed to fetch stocks within the fund.")
