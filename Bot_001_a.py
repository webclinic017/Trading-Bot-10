import alpaca_trade_api as tradeapi
from datetime import date
import time
import datetime



BASE_URL = 'https://paper-api.alpaca.markets'
PUB_KEY = 'PK23SND8QLZ211MQPQXI'
SEC_KEY = '97t5BjP9Ugmym4404zPqRL2js2RWs9PZXt3dhbOr'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


ticker = "FAS"

trading = True; days = 1
# making a loop that will last for 3 days
while trading:
    print("Day {}.".format(days))
    
    # waiting for the day to change
    todayDate = date.today() # setting todays date
    times = 0 # for testing reasons it will loop 3 times.
    while date.today() == todayDate: # if it is still the same day it will stay up here in the code
        print('still the same day')
        times += 1
        if times == 3:
            todayDate = 'not today'
        time.sleep(.25) # sleeping for 0.5 second so it isn't freaking out
        
    print('the day changed')

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset(ticker, 'day', limit=5)
    open_price = barset[ticker][-1].c
    print('previous day close {}.'.format(open_price))


    clock = api.get_clock()
    times = 0
    while not clock.is_open:
        times += 1
        print('still isn''t open')
        if times == 3:
            break
        
    print('the market opened up')
    

        
    days += 1
    if days == 4:
        trading = False
    
    print()


