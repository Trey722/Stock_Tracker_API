from OPTIONS import options_dependencies
from OPTIONS import option_object



def calculate_profit(staring_price, ending_price, step, ticker, buy = True):
    detials = {}
    option = option_object.option_object(ticker)
    x = staring_price
    while (x <= ending_price):
        if buy == True:
            profit = option.calculate_value_at_expiration_buy(option.get_permium(), x)
        else:
            profit = option.calculate_value_at_expiration_seller(option.get_permium(), x)
        detials[x] = profit
        x += step
        
    return detials
    