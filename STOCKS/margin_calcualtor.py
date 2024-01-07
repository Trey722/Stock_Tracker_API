



#--calculate STOCK MARGIN {quantity} {underlying_buy_price} {margin_used} {start_price} {end_price} {step}
def calculate_margin(quantity, underlying_buy_price, margin_used, start_price, end_price, step):
    results = {}
    
    curPrice = start_price
    while 0 <= curPrice <= end_price:
        revanue = quantity * curPrice
        cost = underlying_buy_price * quantity
        print(revanue, cost)
        gross_profit = revanue - cost
        result = gross_profit - margin_used
        results[curPrice] = result
        
        curPrice += step
        
    return results


        
    