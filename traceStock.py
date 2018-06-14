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
    stock_list = ['601990', '603666']
    for code in stock_list:
        df = ts.get_realtime_quotes(code)
        row = next(df.iterrows())[1]
        price = row['price']
        name = row['name']
        try:
            record = Stock.select().where(Stock.code==code).get()
            record.today_price = price
            record.save()
        except Stock.DoesNotExist:
            Stock(code=code, name=name, today_price=price).save()
        print(code, name, price)

if __name__ == "__main__":
    init_recent_stock()

