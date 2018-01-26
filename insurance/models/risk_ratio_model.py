# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Risk_ratio model
"""

import csv
from utils.data_util import load_data
from models.core.dnn_model import Dnn


def train_risk_ratio(data_path, data_type, metrics_path):
    """

    :param data_path: 数据路径
    :param data_type: 数据类型
    :param metrics_path: loss记录路径
    :return:
    """

    risk_feature_cat = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    risk_feature_con = ['log_amount', 'log_num', 'sex_ratio']
    risk_label = 'risk_ratio'
    risk_train, risk_validate, risk_test = \
        load_data(data_path, data_type, risk_feature_cat, risk_feature_con, risk_label)

    risk_model_path = data_path + 'insurance_price/keras_risk_ratio/'
    risk_metrics_file = metrics_path + 'risk_ratio_metrics.csv'
    dnn = Dnn(risk_model_path)
    dnn.dnn_net(input_shape=177)
    dnn.train_model(risk_metrics_file, risk_train, risk_label, epoch=150)
    dnn.save_model()
    # 出险率训练集
    risk_train_y, risk_train_yp = dnn.predict(risk_train, risk_label)
    risk_train_error = dnn.cal_error(risk_train_y, risk_train_yp)
    # 出险率验证集
    risk_validate_y, risk_validate_yp = dnn.predict(risk_validate, risk_label)
    risk_validate_error = dnn.cal_error(risk_validate_y, risk_validate_yp)
    dnn.save_result(risk_model_path, risk_validate_y, risk_validate_yp)
    # 出险率测试集
    risk_test_y, risk_test_yp = dnn.predict(risk_test, risk_label)
    risk_test_error = dnn.cal_error(risk_test_y, risk_test_yp)

    with open(risk_metrics_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['训练集', ' '.join(str(i) for i in risk_train_error)])
        writer.writerow(['验证集', ' '.join(str(i) for i in risk_validate_error)])
        writer.writerow(['测试集', ' '.join(str(i) for i in risk_test_error)])

    fmt = '%6.3f' * 3
    print('出险率：', '训练集', fmt % risk_train_error,
          '验证集', fmt % risk_validate_error,
          '测试集', fmt % risk_test_error)


