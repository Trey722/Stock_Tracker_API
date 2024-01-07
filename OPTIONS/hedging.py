from decimal import Decimal, ROUND_HALF_UP, getcontext




def gamma_hedge_simple(quantity, delta_percent_original, gamma_percent_original,delta, gamma_hedge_percent):
    getcontext().prec = 28  # Set precision
    quantity = Decimal(quantity)
    delta_percent_original = Decimal(delta_percent_original)
    gamma_percent_original = Decimal(gamma_percent_original)
    gamma_hedge_percent = Decimal(gamma_hedge_percent)
    delta = Decimal(delta)

    position_delta = quantity * delta_percent_original
    position_gamma = quantity * gamma_percent_original

    quantity_buy = (position_gamma / gamma_hedge_percent) * -1
    

    trade_delta = delta * quantity_buy
    quantity_delta_net = trade_delta + position_delta
    return {"option": int(quantity_buy),
            "stock": float(quantity_delta_net.quantize(Decimal('1'), rounding=ROUND_HALF_UP))}
    
#print(gamma_hedge_simple('-10000', '0.550', '0.04400', '0.03650', '0.270'))
    
    




    
    
    
    