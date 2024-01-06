from OPTIONS import option_object
from STOCKS import stock_data
import FRED.get_fred_data
import json


option = option_object.option_object('AAPL240112C00060000')

print(json.dumps(option.get_greeks()))





