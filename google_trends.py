# -*- coding: utf-8 -*-

from pytrends.request import TrendReq
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import style

style.use('ggplot')

"""
For some Wierd reason Google will return daily data for request of maximum 8 months.
For 9 months it returns weekly data.
"""

dates_list = ['2014-01-01 2014-09-01',
        '2014-09-01 2015-05-01',
        '2015-05-01 2016-01-01',
        '2016-01-01 2016-09-01',
        '2016-09-01 2017-05-01',
        '2017-05-01 2018-01-01',
        '2018-01-01 2018-04-08',   
        ]

kw_list = ["Blockchain", "Bitcoin", "Etherium", "crypto", "cryptocurrency"]

trends_df = []

for d in dates_list:
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe=d, geo='', gprop='')
    trends_df.append(pytrends.interest_over_time())
    time.sleep(2)

trends_df = pd.DataFrame().append(other=trends_df)
trends_df = trends_df.loc[~trends_df.index.duplicated()]

trends_df.to_csv("google_trends_stats.csv")

trends_df['2017-06':'2018-03'].Bitcoin.plot(
        kind='line', 
        figsize=(12,6),
        title='Google Trends',
        style='b-', 
        use_index=True)

