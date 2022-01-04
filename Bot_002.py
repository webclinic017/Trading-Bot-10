#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 14:53:27 2022

@author: tayloredwinnichols
""" 

import alpaca_trade_api as tradeapi
from datetime import date
import time
import datetime
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pandas_ta as ta


BASE_URL = 'https://paper-api.alpaca.markets'
PUB_KEY = 'PK92I7HHN7R3TNHJSJG8'
SEC_KEY = 'To6M3zJRMYfaBriBAtPru9E2uSg7MnwPLiy5CO4G'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)





## Making a function that takes in ticker and outputs df with ti ##
def getDF(ticker, LIMIT):
    # Load data
    df = api.get_barset(ticker, 'day', limit=LIMIT).df
    df = df.set_axis(['open', 'high', 'low', 'close', 'volume'], axis=1, inplace=False)

    # add data points
    df['sma10'] = df.ta.sma(length=10)
    df['williams'] = df.ta.willr()

    df = df[[
            'open','close','sma10','williams'
            ]]

    df = df.dropna()
    df.reset_index(inplace=True)
    
    return df



## check market time ##
def time_to_market_close():
    clock = api.get_clock()
    return (clock.next_close - clock.timestamp).total_seconds()/60




## check to see if any of tickers have buy signals ##
def should_buy(tickers):
    des = []
    for ticker in tickers:
        data = getDF(ticker, 60)
        if data.iloc[-1]['williams'] < -80:
            des.append([ticker,True])
        else:
            des.append([ticker,False])
    return des



## check to see if any of tickers have sell signals ##
def should_sell(tickers):
    des = []
    for ticker in tickers:
        data = getDF(ticker, 60)
        if data.iloc[-1]['williams'] > -20:
            des.append([ticker,True])
        else:
            des.append([ticker,False])
    return des



## check to see if there is a position in ticker ##
def does_pos(ticker):
    portfolio = api.list_positions()
    pos_owned = []
    for position in portfolio:
        pos_owned.append(position.symbol)
    state = ticker in pos_owned
    return state




## tickers to use ##
tickers = ["SOXL","FAS","FNGU","TNA","LABU","YINN","DPST","NAIL",\
           "DFEN","DUSL","MIDU","MEXX","PILL","RETL","TPOR","KORU"]



## the start of the program will update us on a few things ##
account = api.get_account()
print("Account number: {}".format(account.account_number))
print("Buying power: ${}".format(account.buying_power))
print("Cash available: ${}".format(account.cash))
print('${} allowed for each ticker, or {}%.'.format(float(account.cash)/len(tickers),100/len(tickers)))
print("status: {}".format(account.status))
print("trading blocked: {}".format(account.trading_blocked))
print()

## check current positions ##
# Get a list of all of our positions.
portfolio = api.list_positions()
# Print the quantity of shares for each position.
for position in portfolio:
    print("I own {} shares of {}.".format(position.qty, position.symbol))

print()
print()


## main loop that runs. it waits will there is 15 minutes left in the trading day ##
minutes = time_to_market_close()
while minutes > 15:
    minutes = time_to_market_close()
    time.sleep(180)
    print("minutes left: {}".format(round(minutes,1)))
    print("hours left: {}".format(round(minutes,1)/60))
    
print()    
print('it left the loop!!')
print()




## should I buy any tickers?? ##
des1 = should_buy(tickers)
for d in des1:
    print("Buying descision: {} for ticker: {}.".format(d[1], d[0]))
print()
print()


## should I sell any tickers?? ##
des2 = should_sell(tickers)
for d in des2:
    print("Selling descision: {} for ticker: {}.".format(d[1], d[0]))
print()
print()


## if we do not own the ticker, buy order ##
account = api.get_account()
for i in des1:
    if i[1] == True and does_pos(i[0]) == False:
        
        # figuring out how many shares to buy #
        last_price = api.get_last_trade(i[0]).price
        order_amount = int(((float(account.cash)/len(tickers))*.95)/last_price)
        
        # Buy a stock
        api.submit_order(
          symbol=i[0], # Replace with the ticker of the stock you want to buy
          qty=order_amount,
          side='buy',
          type='market', 
          time_in_force='day' # day
        )
        
        print("place buy order for {} and {} shares.".format(i[0], order_amount))

print()
print()

## if we do own the ticker, sell order ##
for i in des2:
    if i[1] == True and does_pos(i[0]) == True:
        
        # how many shares to sell #
        order_amount = int(api.get_position(i[0]).qty)
        
        api.submit_order(
          symbol=i[0], # Replace with the ticker of the stock you want to buy
          qty=order_amount,
          side='sell',
          type='market', 
          time_in_force='gtc' # Good 'til cancelled
        )
        
        print("place sell order for {} and {} shares.".format(i[0], order_amount))


print()
print()

## print information after script has ran ##
## list orders and details ##
orders = api.list_orders()
print("{} orders in.".format(len(orders)))
for o in orders:
    print("Sell {} shares of {} on {}.".format(o.qty, o.symbol, o.time_in_force))














