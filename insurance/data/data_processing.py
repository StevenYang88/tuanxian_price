# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Data processing
"""

import math
import pandas as pd


def classify_age(avg_age):
    """
    划分年龄
    :param avg_age: 平均年龄
    :return: 年龄段
    """
    age_list = [0, 19, 36, 46, 56, 61, 66]
    for index, value in enumerate(age_list):
        if float(avg_age) < value:
            return index
    return len(age_list)


if __name__ == '__main__':

    data_type = {'policy': str, 'coverage': str, 'industry': str, 'occupation': str, 'city': str,
                 'amount': float, 'num': int, 'avg_age': float, 'sex_ratio': float,
                 'risk_ratio': float, 'avg_pay': float, 'avg_claim': float, 'avg_days': float}
    df = pd.read_csv('data_1220.csv', low_memory=True, dtype=data_type)
    features = ['company', 'policy', 'coverage', 'industry', 'occupation', 'city', 'amount',
                'num', 'avg_age', 'sex_ratio']
    labels = ['risk_ratio', 'avg_pay', 'avg_claim', 'avg_days']
    # 提取原始数据
    df = df[features + labels]
    # 去除空行
    for feature in features:
        df = df[~df[feature].isnull()]
    # 填充空值
    df = df.fillna(0)
    # 以万为单位
    df['avg_pay'] = df['avg_pay'] / 10000
    df['avg_claim'] = df['avg_claim'] / 10000
    # 年龄分区
    df['avg_age'] = [classify_age(s) for s in df['avg_age']]
    # 保存数据
    df.to_csv('data_raw.csv', float_format='%.2f', index=False)
    # 对数变换
    df['log_amount'] = df['amount'].apply(lambda x: math.log10(x))
    df['log_num'] = df['num'].apply(lambda x: math.log10(x))
    # 打乱顺序
    df = df.sample(frac=1)
    # 训练集和验证集
    df_1 = df[0:int(len(df)*0.9)]
    df_1 = df_1[df_1['num'] > 10]
    df_1 = df_1[df_1['risk_ratio'] < 100]
    df_1.to_csv('data_raw_1.csv', float_format='%.2f', index=False)
    # 测试集
    df_0 = df[int(len(df)*0.9):]
    df_0.to_csv('data_raw_2.csv', float_format='%.2f', index=False)
