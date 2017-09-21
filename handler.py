
import pandas as pd
from pandas import Series
from pandas.tseries.offsets import BDay
import tushare as ts


def count_stocks(labels, stocks):
    nlist = []
    exists = []
    reserved = []
    for label, stock in zip(labels, stocks):
        nlist.extend(stock.keys())

    scount = Series(nlist).value_counts()
    print(scount)
    res = scount[scount > 2].index
    endtime = pd.datetime.today()
    starttime = endtime - BDay(4)
    starttime = starttime.strftime('%Y-%m-%d')
    endtime = endtime.strftime('%Y-%m-%d')

    for i in res:
        hist = ts.get_hist_data(code=i, start=starttime, end=endtime)
        print(hist)
        # print(i)
        if hist is not None:
            l = len(hist)
            if hist['close'].mean() < 15 and l > 3:
                test = [abs(hist['close'][i] - hist['close'][i-1])< 0.3
                        for i in range(1, 4)]
                if all(test):
                    reserved.append(i)

    # print(reserved)
    return reserved

if __name__ == '__main__':
    s1 = ['创金合信鑫收', '招商国企改革']
    s2 = [{'sh600016': '民生银行', 'sh601988': '中国银行', 'sz002142': '宁波银行', 'sh601166': '兴业银行', 'sz000001': '平安银行', 'sz000830': '鲁西化工', 'sh601601': '中国太保', 'sh600816': '安信信托', 'sh601398': '工商银行', 'sh601939': '建设银行'}, {'sh601668': '中国建筑', 'sh600068': '葛洲坝', 'sh603993': '洛阳钼业', 'sz002460': '赣锋锂业', 'sz002466': '天齐锂业', 'sh601601': '中国太保', 'sh603799': '华友钴业', 'sz002089': '新海宜', 'sz000980': '众泰汽车', 'sz000065': '北方国际'}]
    count_stocks(s1, s2)