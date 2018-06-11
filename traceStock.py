# -*- coding: utf-8 -*-  
"""  
 @date: 2018/6/7
 @author: wdj  
 @desc:
"""
import tushare as ts
import time

while True:
    df = ts.get_realtime_quotes('600136')
    print(df[['price', 'bid', 'ask', 'volume', 'amount', 'time']])
    time.sleep(2)
