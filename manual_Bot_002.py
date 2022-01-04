#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 21:37:05 2022

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
import yfinance as yf


BASE_URL = 'https://paper-api.alpaca.markets'
PUB_KEY = 'PK92I7HHN7R3TNHJSJG8'
SEC_KEY = 'To6M3zJRMYfaBriBAtPru9E2uSg7MnwPLiy5CO4G'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)




## getting data ##
def getDB(ticker):
    tick = ticker
    # Load data
    data = yf.Ticker(tick)
    df = data.history(period="6mo", interval="1d")
#     df = data.history(start="2018-12-01", end="2020-03-01")
#     start="2017-01-01", end="2017-04-30"
    
    # add data points
    df['close_per1'] = df.ta.percent_return(1)*100
    df['sma10'] = df.ta.sma(length=10)
    df['williams'] = df.ta.willr(7)


    df = df[[
            'open','close','sma10','williams'
            ]]

    df = df.dropna()
    df.reset_index(inplace=True)
    
    return df



# tickers = ["SOXL","SPXL","TECL","FAS","UPRO","FNGU","TNA","LABU","YINN","DPST","NAIL","DFEN","CURE","EURL","DUSL","MIDU","EDU","MEXX","PILL","DRN","RETL","TPOR","UTSL","KORU","OILU"]

tickers = ["SOXL","FAS","FNGU","TNA","LABU","YINN","DPST","NAIL","DFEN","DUSL","MIDU","MEXX","PILL","RETL","TPOR","KORU"]

for ticker in tickers:
    print()
    print("ticker: {}".format(ticker))
    df = getDB(ticker)
    williams = df.iloc[-1]['williams']
    
    ## Williams trading idea ##
    if williams < -80:
        print("buy {}, williams = {}".format(ticker, williams))
    elif williams > -20:
        print("sell {}, williams = {}".format(ticker, williams))
    else:
        print("do nothing for {}".format(ticker))



