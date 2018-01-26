# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Data distributions
"""

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'data_raw_1.csv'
data_type = {'policy': str, 'coverage': str, 'industry': str, 'occupation': str, 'city': str,
             'log_amount': float, 'log_num': float, 'avg_age': float, 'sex_ratio': float,
             'risk_ratio': float, 'avg_pay': float, 'avg_claim': float, 'avg_days': float}

df = pd.read_csv(data_path, low_memory=True, dtype=data_type)

plt.figure(1)
# 保额取对数分布图
plt.subplot(221)
plt.hist(df['log_amount'], 30)
plt.xlabel('log_amount')
plt.subplot(222)
# 平均年龄分布图
plt.hist(df['avg_age'], 30)
plt.xlabel('avg_age')
plt.subplot(223)
# 男性占比分布图
plt.hist(df['sex_ratio'], 30)
plt.xlabel('sex_ratio')
plt.subplot(224)
# 投保人数取对数分布图
plt.hist(df['log_num'], 30)
plt.xlabel('log_num')
plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.35, bottom=0.15, top=0.90)
plt.show()

print(df['log_num'].mean())
print(df['log_num'].std())

