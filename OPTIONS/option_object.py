import yfinance as yf 
import STOCKS.stock_data

import math
import FRED.get_fred_data
from OPTIONS import calculate_greeks,options_dependencies
import QuantLib as ql
from GENERAL import extract_date

class option_object:
    def __init__(self, option_string : str):
        option_data = options_dependencies.get_option_data(option_string)
        
        self.underlying_ticker = option_data['ticker']
        self.experiation_date =  option_data['experiation_date']
        self.type = option_data['type']
        self.strike = option_data['strike']
        self.expiry_date = extract_date.get_date(option_data['experiation_date'])
        
        
    
    
        
    def get_underlying_value(self):
        return STOCKS.stock_data.get_stock_price(self.underlying_ticker)
    
    
    
    
    def get_type(self):
        if (self.type == "C"):
            return ql.Option.Call
        return ql.Option.Put
    
    
    def get_greeks(self):
       
        greeks = calculate_greeks.calculate_option_greeks(self.get_type(), self.get_underlying_value(), self.strike, ql.Date(self.expiry_date['day'], self.expiry_date['month'], self.expiry_date['year']), self.get_voltiaility(), FRED.get_fred_data.get_risk_free_intrest_rate(), STOCKS.stock_data.get_dividends_recent(self.underlying_ticker))
        return greeks

    
    
    
    def calculate_value_at_expiration_buy(self, perimium : float, underlying_price : float) -> float:
        cost = -1 * perimium
        if self.type == "C":
            value = (underlying_price - self.strike) * 100
            profit = value - perimium
            
        elif self.type == "P":
            value = (self.strike - underlying_price) * 100
        
        if profit < cost:
            return cost
        else:
            return profit
        
        
    def get_data(self):
        return options_dependencies.get_option(self.underlying_ticker, self.strike, self.experiation_date)
    
    
    def get_voltiaility(self):
        data = self.get_data()['impliedVolatility']
        return float(data.item())
    
    def get_permium(self):
        data = self.get_data()['ask']
        return float(data.item())
        
        
    # Just the inverse 
    def calculate_value_at_expiration_seller(self, perimium : float, underlying_price : float) -> float:
        return self.calculate_value_at_expiration_buy(perimium, underlying_price) * -1
    
    # Estimates 0 change in voltaility 
    # Date needs to be written in as YYYYMMDD no hyphens as an int
    def calculate_value_before_expiration(self, underlying_price : float, date : int) -> float:
        current_price = underlying_price
        K = self.strike
        T = options_dependencies.delta_time(date, self.experiation_date)
        r = FRED.get_fred_data.get_risk_free_intrest_rate()
        sigma = 0.178
        type = self.type
        
        return options_dependencies.black_scholes(current_price, K, T, r, sigma, type)
        