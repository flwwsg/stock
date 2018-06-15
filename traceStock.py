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
import json
import logging

db = SqliteDatabase("stock.db")
logging.basicConfig()


class Stock(Model):
    code = CharField(primary_key=True, max_length=6)
    name = CharField(max_length=40)
    published_date = DateTimeField()
    published_price = FloatField(default=0)
    today_price = FloatField()
    updated = DateTimeField()
    auto = BooleanField(default=True)

    class Meta:
        database = db


class Monitor(Model):
    code = CharField(primary_key=True, max_length=6)
    auto = BooleanField(default=True)
    updated = DateTimeField()

    class Meta:
        database = db


def stock_tick(code):
    """
    monitoring stock
    :param code:
    :return:
    """
    while True:
        df = ts.get_realtime_quotes(code)
        print(df[['price', 'bid', 'ask', 'volume', 'amount', 'time']])
        time.sleep(2)


def check_recent_stock(price):
    code_to_check = []
    for row in Stock.select():
        today_price = get_today_price(row.code)
        if today_price == 0:
            continue
        if today_price < price or 0 < row.published_price < price:
            if check_recent_stock_below_days(row.code):
                code_to_check.append(row.code)
    for row in  Monitor.select():
        if row.auto:
            row.delete_instance()
        else:
            row.updated = datetime.datetime.now()
            row.save()
            if row.code in code_to_check:
                code_to_check.remove(row.code)

    for code in code_to_check:
        Monitor.create(code=code, auto=True, updated=datetime.datetime.now())

    return code_to_check


def check_recent_stock_below_days(code):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=10)
    hist = ts.get_hist_data(code=code, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'))
    if hist is None or len(hist) < 7 :
        return False
    for j in range(1, 7):
        test = hist['close'][j] < hist['close'][j - 1] or abs(hist['close'][j] - hist['close'][j - 1]) < 1
        if not test:
            return False
    return True


def add_or_update_recent_stock(code, name, publish_date=None, publish_price=0, today_price=0, auto=True):
    """
    add or update recent published stock
    :param code:
    :param name:
    :param publish_date:
    :param publish_price:
    :param today_price:
    :param auto:
    :return:
    """
    try:
        record = Stock.get(Stock.code == code)
        record.today_price = today_price
        record.updated = datetime.datetime.now()
        record.save()
    except Stock.DoesNotExist:
        Stock.create(code=code, name=name, today_price=today_price, published_date=publish_date,
                     published_price=publish_price, updated=datetime.datetime.now(), auto=auto)


def init_recent_stock():
    """
    initialization recent stock, running only once
    :return:
    """
    if Stock.table_exists():
        Stock.drop_table()
    if Monitor.table_exists():
        Monitor.drop_table()
    Stock.create_table()
    Monitor.create_table()
    # assume no error occur in loading json
    recent = json.load(open('recent_stock.json'))
    for stock in recent:
        code = stock[0]
        publish_date = stock[1]
        publish_price = stock[2]
        if check_published_date(publish_date, 365):
            # ignore stock after one year
            return
        row  = get_today_stock_info(code)
        if row is None:
            continue
        today_price = row['price']
        name = row['name']
        add_or_update_recent_stock(code, name, publish_date, publish_price, today_price)


# helper function
def parse_date(time_str):
    try:
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d")
    except ValueError:
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return dt.date()


def get_today_price(code):
    row = get_today_stock_info(code)
    if row is None:
        return 0
    return row['price']


def get_today_stock_info(code):
    try:
        df = ts.get_realtime_quotes(code)
    except Exception:
        logging.error("error in %s" % code)
        return None
    return next(df.iterrows())[1]


def check_published_date(published_date, interval=365):
    p_date = parse_date(published_date)
    now_date = datetime.datetime.now().date()
    cmp = now_date - p_date
    if cmp.days > interval:
        return True
    return False


if __name__ == "__main__":
    init_recent_stock()
    # stock_tick("603993")
    # print(check_recent_stock_below_days("603993"))
