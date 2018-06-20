# -*- coding: utf-8 -*-  
"""  
 @date: 2018/6/7
 @author: wdj  
 @desc:
"""
import tushare as ts
import time
import datetime
from peewee import CharField, SqliteDatabase, DateTimeField, FloatField,  BooleanField, Model
import json
import logging
from collections import namedtuple

db = SqliteDatabase("stock.db")
logging.basicConfig()
MAX_STOCK = 5


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
    name = CharField(max_length=40)
    today_price = FloatField()

    class Meta:
        database = db


def stock_tick(code=""):
    """
    monitoring stock
    :param code:
    :return:
    """
    if code != "":
        add_stock_to_monitor(code, auto=True)
    codes = [row.code for row in Monitor.select()]
    if len(codes) == 0:
        logging.error("nothing to monitor")
        return
    if len(codes) > MAX_STOCK:
        logging.error("too much (greater than %s) stock to monitor" % MAX_STOCK)
        return
    while True:
        df = ts.get_realtime_quotes(codes)
        print(df[['name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']])
        time.sleep(2)


def add_stock_to_monitor(code, auto):
    try:
        Monitor.get(code=code)
    except Monitor.DoesNotExist:
        Monitor.create(code=code, auto=auto, updated=datetime.datetime.now())


def check_recent_stock(base_price):
    code_to_check = []
    stock = namedtuple("stock", ["code", "name", "today_price"])
    remain = []
    for row in  Monitor.select():
        if row.auto:
            row.delete_instance()
        else:
            remain.append(row.code)
    for row in Stock.select():
        today_price = get_today_price(row.code)
        if today_price == 0:
            continue
        if today_price < base_price or today_price < float(row.published_price) < base_price:
            if check_recent_stock_below_days(row.code):
                r = stock(row.code, row.name, today_price)
                print("selected code is %s, today_price is %s, published_price is %s, base price is %s" % (r.name, r.today_price, row.published_price, base_price))
                if row.code not in remain:
                    code_to_check.append(r)
                else:
                    row.updated = datetime.datetime.now()
                    row.today_price = today_price
                    row.save()

    for row in code_to_check:
        Monitor.create(code=row.code, name=row.name, today_price=row.today_price, auto=True, updated=datetime.datetime.now())

    return code_to_check


def check_recent_stock_below_days(code):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=10)
    hist = ts.get_hist_data(code=code, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'))
    if hist is None or len(hist) < 5 :
        return False
    for j in range(1, 5):
        test = hist['close'][j-1] < hist['close'][j] or abs(hist['close'][j] - hist['close'][j - 1]) < 1
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
    return float(row['price'])


def get_today_stock_info(code):
    try:
        df = ts.get_realtime_quotes(code)
    except Exception:
        logging.error("error in %s" % code)
        return None
    if df is None:
        logging.error("today stock %s is none" % code)
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
    # check_recent_stock(10)
    stock_tick()
