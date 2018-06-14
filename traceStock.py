# -*- coding: utf-8 -*-  
"""  
 @date: 2018/6/7
 @author: wdj  
 @desc:
"""
import tushare as ts
import time
import datetime
from peewee import *


db = SqliteDatabase("stock.db")

class Stock(Model):
    code = CharField(primary_key=True, max_length=6)
    name = CharField(max_length=40)
    publish_date = DateTimeField(default=datetime.datetime.now())
    publish_price = FloatField(default=0)
    today_price = FloatField()
    
    class Meta:
        database = db

def stock_tick(code):
    while True:
        df = ts.get_realtime_quotes(code)
        print(df[['price', 'bid', 'ask', 'volume', 'amount', 'time']])
        time.sleep(2)

def check_recent_stock():
    pass


def init_recent_stock():
    if db.table_exists(Stock):
        db.drop_tables([Stock])
        print("table exists")
    db.create_tables([Stock])
    stock_list = ['603666', '601330', '603486', '603045', '603013', '603259', '603596', '603348', '603733', '603876', '603773', '603301',
        '603897', '002931', '603214', '002930', '600929', '002928', '002929', '603059', '600901', '603680', '603712', '002927', '603506', '603356','603056',
        '603655', '002923', '603848', '603809'
        ]
    for code in stock_list:
        try:
            df = ts.get_realtime_quotes(code)
        except Exception:
            print("error in %s" % code)
            continue
        row = next(df.iterrows())[1]
        price = row['price']
        name = row['name']
        try:
            record = Stock.select().where(Stock.code==code).get()
            record.today_price = price
            record.save()
        except Stock.DoesNotExist:
            Stock(code=code, name=name, today_price=price).save()
        # print(code, name, price)
        if float(price) < 30:
            print(code, name, price)

if __name__ == "__main__":
    init_recent_stock()

