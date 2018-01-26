# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Avg_days model
"""

import csv
from utils.data_util import load_data
from models.core.dnn_model import Dnn


def train_avg_days(data_path, data_type, metrics_path):
    """

    :param data_path: 数据路径
    :param data_type: 数据类型
    :param metrics_path: loss记录路径
    :return:
    """

    days_feature_cat = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    days_feature_con = ['log_amount', 'log_num', 'sex_ratio']
    days_label = 'avg_days'
    days_train, days_validate, days_test = \
        load_data(data_path, data_type, days_feature_cat, days_feature_con, days_label)

    days_model_path = data_path + 'insurance_price/keras_avg_days/'
    days_metrics_file = metrics_path + 'avg_days_metrics.csv'

    dnn = Dnn(days_model_path)
    dnn.dnn_net(input_shape=177)
    dnn.train_model(days_metrics_file, days_train, days_label, epoch=150)
    dnn.save_model()
    # 出险率训练集
    days_train_y, days_train_yp = dnn.predict(days_train, days_label)
    days_train_error = dnn.cal_error(days_train_y, days_train_yp)
    # 出险率验证集
    days_validate_y, days_validate_yp = dnn.predict(days_validate, days_label)
    days_validate_error = dnn.cal_error(days_validate_y, days_validate_yp)
    dnn.save_result(days_model_path, days_validate_y, days_validate_yp)
    # 出险率测试集
    days_test_y, days_test_yp = dnn.predict(days_test, days_label)
    days_test_error = dnn.cal_error(days_test_y, days_test_yp)

    with open(days_metrics_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['训练集', ' '.join(str(i) for i in days_train_error)])
        writer.writerow(['验证集', ' '.join(str(i) for i in days_validate_error)])
        writer.writerow(['测试集', ' '.join(str(i) for i in days_test_error)])

    fmt = '%6.3f' * 3
    print('平均住院天数：', '训练集', fmt % days_train_error,
          '验证集', fmt % days_validate_error,
          '测试集', fmt % days_test_error)
