import QuantLib as ql

def calculate_theta_per_day(option, today,price,risk_free_rate,volatility, step=1):
    # Calculate option price for the current time (t0)
    option.setPricingEngine(ql.AnalyticEuropeanEngine(ql.BlackScholesMertonProcess(
        ql.QuoteHandle(ql.SimpleQuote(price)),
        ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, ql.Actual360())),
        ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), option.volatility, ql.Actual360()))
    )))
    price_t0 = option.NPV()

    # Calculate option price for a slightly later time (t1 = t0 + step)
    new_date = today + ql.Period(step, ql.Days)
    ql.Settings.instance().evaluationDate = new_date
    option.setPricingEngine(ql.AnalyticEuropeanEngine(ql.BlackScholesMertonProcess(
        ql.QuoteHandle(ql.SimpleQuote(option.underlyingPrice)),
        ql.YieldTermStructureHandle(ql.FlatForward(new_date, option.riskFreeRate, ql.Actual360())),
        ql.BlackVolTermStructureHandle(ql.BlackConstantVol(new_date, ql.NullCalendar(), volatility, ql.Actual360()))
    )))
    price_t1 = option.NPV()

    # Calculate theta per day as the change in option price divided by the change in time (step)
    theta_per_day = (price_t1 - price_t0) / step
    return theta_per_day

def calculate_option_greeks(option_type, underlying_price, strike_price, expiry_date, volatility, risk_free_rate, dividend_rate):
    today = ql.Date(4, 1, 2024)  # Replace with the current date
    ql.Settings.instance().evaluationDate = today
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.AmericanExercise(today, expiry_date)
    option = ql.VanillaOption(payoff, exercise)

    spot_handle = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, ql.Actual360()))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_rate, ql.Actual360()))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), volatility, ql.Actual360()))

    bs_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
    option.setPricingEngine(ql.BinomialVanillaEngine(bs_process, "crr", 100))

    delta = option.delta()
    gamma = option.gamma()
   

    greeks_dict = {
        "Delta": delta,
        "Gamma": gamma,

    }

    return greeks_dict