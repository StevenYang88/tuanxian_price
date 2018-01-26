# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Avg_pay model
"""

import csv
from utils.data_util import load_data
from models.core.dnn_model import Dnn


def train_avg_pay(data_path, data_type, metrics_path):
    """

    :param data_path: 数据路径
    :param data_type: 数据类型
    :param metrics_path: loss记录路径
    :return:
    """

    pay_feature_cat = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    pay_feature_con = ['log_amount', 'log_num', 'sex_ratio']
    pay_label = 'avg_pay'
    pay_train, pay_validate, pay_test = \
        load_data(data_path, data_type, pay_feature_cat, pay_feature_con, pay_label)

    pay_model_path = data_path + 'insurance_price/keras_avg_pay/'
    pay_metrics_file = metrics_path + 'avg_pay_metrics.csv'

    dnn = Dnn(pay_model_path)
    dnn.dnn_net(input_shape=177)
    dnn.train_model(pay_metrics_file, pay_train, pay_label, epoch=150)
    dnn.save_model()
    # 出险率训练集
    pay_train_y, pay_train_yp = dnn.predict(pay_train, pay_label)
    pay_train_error = dnn.cal_error(pay_train_y, pay_train_yp)
    # 出险率验证集
    pay_validate_y, pay_validate_yp = dnn.predict(pay_validate, pay_label)
    pay_validate_error = dnn.cal_error(pay_validate_y, pay_validate_yp)
    dnn.save_result(pay_model_path, pay_validate_y, pay_validate_yp)
    # 出险率测试集
    pay_test_y, pay_test_yp = dnn.predict(pay_test, pay_label)
    pay_test_error = dnn.cal_error(pay_test_y, pay_test_yp)

    with open(pay_metrics_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['训练集', ' '.join(str(i) for i in pay_train_error)])
        writer.writerow(['验证集', ' '.join(str(i) for i in pay_validate_error)])
        writer.writerow(['测试集', ' '.join(str(i) for i in pay_test_error)])

    fmt = '%6.3f' * 3
    print('件均赔付：', '训练集', fmt % pay_train_error,
          '验证集', fmt % pay_validate_error,
          '测试集', fmt % pay_test_error)
