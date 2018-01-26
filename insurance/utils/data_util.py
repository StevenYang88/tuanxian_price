# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Load data and calculate the acc of results.
"""

import numpy as np
import pandas as pd
from utils.encoder import Encode
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path, d_type, feature_cat, feature_con, label):
    """
    加载数据
    :param path: 数据路径
    :param d_type: 数据类型
    :param feature_cat: 类别特征
    :param feature_con: 数值特征
    :param label: 数据标签
    :return: 训练集，验证集，测试集
    """
    file_1 = 'data_raw_1.csv'  # 训练集和验证集数据文件
    file_2 = 'data_raw_2.csv'  # 测试集数据文件
    # 读取数据
    df_1 = pd.read_csv(path + file_1, low_memory=True, dtype=d_type)
    df_2 = pd.read_csv(path + file_2, low_memory=True, dtype=d_type)
    # 训练集和验证集编码
    encode = Encode(path=path, file=file_1, feature_list=feature_cat)
    x_cat = encode.feature_encoding()
    x_con = df_1[feature_con]
    scaler = StandardScaler().fit(x_con)
    x_con = pd.DataFrame(scaler.transform(x_con))
    x_data = pd.concat([x_cat, x_con], axis=1)
    y_data = df_1[label]
    # 划分训练集和验证集
    x_train, x_validate, y_train, y_validate = \
        train_test_split(x_data, y_data, test_size=0.2, random_state=0)
    train_set = pd.concat([x_train, y_train], axis=1)
    validate_set = pd.concat([x_validate, y_validate], axis=1)
    # 测试集编码
    encode = Encode(path=path, file=file_2, feature_list=feature_cat)
    x_cat = encode.feature_encoding()
    x_con = df_2[feature_con]
    x_con = pd.DataFrame(scaler.transform(x_con))
    x_test = pd.concat([x_cat, x_con], axis=1)
    y_test = df_2[label]
    test_set = pd.concat([x_test, y_test], axis=1)
    return pd.DataFrame(train_set), pd.DataFrame(validate_set), pd.DataFrame(test_set)


def cal_acc(path):
    """

    :param path: 模型结果路径
    :return: 准确率
    """
    result_file = 'result.csv'  # 模型结果文件
    # 读取数据
    df = pd.read_csv(path + result_file, low_memory=True, dtype=float)
    df['error'] = np.abs(df['yp'] - df['y']) / (df['y'] + 0.1)
    ratios = []
    for item in range(1, 11):
        ratio = df[df['error'] < item * 0.1].count() / df.count()
        ratios.append(round(ratio['error'] * 100, 2))
    ratios = np.array(ratios)
    return ratios


if __name__ == '__main__':
    print(cal_acc('../data/insurance_price/avg_claim/'))
