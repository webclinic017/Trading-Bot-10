import alpaca_trade_api as tradeapi
from datetime import date
import time
import requests
import json
import pandas as pd
from datetime import datetime
from pytz import timezone



## setting api keys and REST ##
BASE_URL = 'https://paper-api.alpaca.markets'
PUB_KEY = 'PK2TSXKJ9TYK7AZOWU18'
SEC_KEY = 'qvQ7zoUULTXkcObXAB6ipBcPSMi5SSUSRBtsFQQw'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


api_key = "af5dfc6f8b230bdf12bfae6008279325"




## getting latest stock prices for tickers ## 
def fetch_most_recent_quote(tickers, api_key):
    responses = []; fail_resp = []
    with requests.session() as session:
        for ticker in tickers:
            resp = session.get(f"https://financialmodelingprep.com/api/v3/quote-short/"+ticker+"?apikey="+api_key)
            try:
                responses.append([resp,resp.json()[0]])
            except:
                responses.append([None,None])
                fail_resp.append(ticker)
                
    return responses, fail_resp


## getting stock proces from the day before ## 
def fetch_day_before_quote(tickers, api_key):
    responses = []; fail_resp = []
    with requests.session() as session:
        for ticker in tickers:
            resp = session.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/"+ticker+"?timeseries=1&apikey="+api_key)
            try:
                responses.append([resp,resp.json()])
            except:
                responses.append([None,None])
                fail_resp.append(ticker)
                
    return responses, fail_resp




## tickers to execute ##
tickers = ["FAS","TNA","SOXL","TECL","LABU","YINN","DPST","NAIL"]

## getting day trading day before close price ##
mrq,fr1 = fetch_most_recent_quote(tickers, api_key)


## the script will loop here untill the market opens ##
clock = api.get_clock() # gets if the market is open
while not clock.is_open:
    ct = clock.timestamp
    
    
print()
print("The market opened up at timestamp: {}.".format(clock.timestamp))
    
    
## getting the first quote of the day ##
dbq,fr2 = fetch_day_before_quote(tickers, api_key)

## formatting the open and close data
close_data = []; open_data = []
for o, c in zip(dbq, mrq):
    close_data.append(c[1]['price'])
    open_data.append(o[1]['historical'][0]['close'])
all_data = {'ticker': tickers, "close_data": close_data, "open_data": open_data}
all_data = pd.DataFrame(all_data)
    
print(all_data)


## figuring out what tickers open higher than the closing day before ##
bid = []
for i in range(len(all_data)):
    if all_data.iloc[i]['close_data'] < all_data.iloc[i]['open_data']:
        bid.append(all_data.iloc[i]['ticker'])
print("I'll be placing bids on these tickers: {}.".format(bid))

   
## placing orders for tickers that passed criteria ## 
for ticker in bid:
    api.submit_order(
            symbol=ticker,
            qty=10,
            side='buy',
            type='market',
            time_in_force='gtc'
        )



## wait until these orders have been filled then loop through then resubmit



# ## waiting till the end of the day before selling aquired shares
# est = timezone('EST')
# current_time = datetime.now(est).strftime("%I:%M")

# while not current_time == "04:20":
#     current_time = datetime.now(est).strftime("%I:%M")
    
## submitting at the close order ##
for ticker in bid:
    api.submit_order(
        symbol=ticker,
        qty=10,
        side='sell',
        type='market',
        time_in_force='cls'
    )
    


print("Program is complete!!")
print("Who knows what happened!!!")







