# -*- coding: utf-8 -*-

import quandl
import pandas as pd
import numpy as np
import os
import sys

from sklearn import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split

data_file = "data/bitcoin_with_alternative_data.csv"

trends_df = pd.read_csv("data/google_trends_stats.csv", index_col = 'date')

trends_df['2017-06':'2018-03'].Bitcoin.interpolate(method='cubic').plot(
        kind='line', 
        figsize=(12,6),
        title='Google Trends',
        style='b-', 
        use_index=True)

if os.path.exists(data_file):
    data = pd.read_csv(data_file, index_col = 'date')
else:
    data = quandl.get("GDAX/USD")
    data.Open['2015':'2016'].plot()
    
    data = data.join(trends_df.Bitcoin)
    
    data['Price'] = (data.High + data.Low) / 2
    data['Spread'] = (data.High - data.Low) 
    data['Pct_change'] = (data.Spread / data.Price) * 100
    data['Pct_Spread'] = (data.Spread / data.Price) * 100
    data.drop('Pct_change', axis=1, inplace=True)
    data.to_csv("data/bitcoin_with_alternative_data.csv")

data['label'] = data.Price.shift(-30)
data = data.dropna()

x = data.drop('label', axis='columns')
y = data.label

x = np.array(x)
y = np.array(y)

scaler = MinMaxScaler((-1, 1))
scaler.fit(x, y)
x = scaler.transform(x)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

clf = linear_model.LinearRegression()
clf.fit(x_train, y_train)
performance = clf.score(x_test, y_test)
print(performance*100)

last = clf.predict(x[-1].reshape(1, -1))

knl_list = ['linear', 'poly', 'rbf', 'sigmoid']

for knl in knl_list: 
    clf = svm.SVR(kernel=knl)
    clf.fit(x_train, y_train)
    performance = clf.score(x_test, y_test)
    print("Performance of {} \t>> {:.3f} %".format(knl, performance*100))

