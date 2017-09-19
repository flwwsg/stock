
import pandas as pd
from pandas import Series
from pandas.tseries.offsets import BDay
import tushare as ts

def count_stocks(labels, stocks):
	nlist = []
	exists = []
	reserved = []
	for label, stock in zip(labels, stocks):
		# if label[:2] in exists:
		# 	continue
		# else:
		# 	exists.append(label[:2])
		nlist.extend(stock.keys())

	scount = Series(nlist).value_counts()
	print(scount)
	res = scount[scount>1].index
	endtime = pd.datetime.today()
	starttime = endtime - BDay(4)
	starttime = starttime.strftime('%Y-%m-%d')
	endtime = endtime.strftime('%Y-%m-%d')

	for i in res:
		hist = ts.get_hist_data(code=i, start=starttime, end=endtime)
		# print(hist)
		print(i)
		if hist is not None:
			l = len(hist)
			if hist['close'].mean() < 20 and l > 3:
				test = [hist['close'][i] > hist['close'][i-1] for i in range(1,4)]
				if all(test):
					reserved.append(i)
	print(reserved)
	print(reserved)
if __name__ == '__main__':
	count_stocks(labels, stocks)