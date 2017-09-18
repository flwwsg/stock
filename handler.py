
import pandas as pd
from pandas import Series
from pandas.tseries.offsets import BDay
import tushare as ts

labels = ['银华领先策略', '鹏华品牌传承']
stocks = [{'sz300021': '大禹节水', 'sz000858': '五粮液', 'sz300274': '阳光电源', 'sz000568': '泸州老窖', 'sz002567': '唐人神', 'sh600809': '山西汾酒', 'sz002640': '跨境通', 'sh600535': '天士力', 'sz000967': '盈峰环境', 'sh600021': '上海电力'}, 
	{'sh600519': '贵州茅台', 'sz002241': '歌尔股份', 'sz000799': '酒鬼酒', 'sz000858': '五粮液', 'sz000651': '格力电器', 'sz000568': '泸州老窖', 'sh603833': '欧派家居', 'sh600779': '水井坊', 'sz002271': '东方雨虹', 'sz002304': '洋河股份'}]

nlist = []
exists = []
for label, stock in zip(labels, stocks):
	if label[:2] in exists:
		continue
	else:
		exists.append(label[:2])
	nlist.extend(stock.keys())

scount = Series(nlist).value_counts()
# print(scount)
res = scount[scount>1].index
endtime = pd.datetime.today()
starttime = endtime - BDay(3)
starttime = starttime.strftime('%Y-%m-%d')
endtime = endtime.strftime('%Y-%m-%d')

for i in res:
	print(i)
	print (ts.get_hist_data(code=i, start=starttime, end=endtime))