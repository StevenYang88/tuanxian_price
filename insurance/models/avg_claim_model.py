# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Avg_claim model
"""

import csv
from utils.data_util import load_data
from models.core.dnn_model import Dnn


def train_avg_claim(data_path, data_type, metrics_path):
    """

    :param data_path: 数据路径
    :param data_type: 数据类型
    :param metrics_path: loss记录路径
    :return:
    """

    claim_feature_cat = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']
    claim_feature_con = ['log_amount', 'log_num', 'sex_ratio']
    claim_label = 'avg_claim'
    claim_train, claim_validate, claim_test = \
        load_data(data_path, data_type, claim_feature_cat, claim_feature_con, claim_label)

    claim_model_path = data_path + 'insurance_price/keras_avg_claim/'
    claim_metrics_file = metrics_path + 'avg_claim_metrics.csv'

    dnn = Dnn(claim_model_path)
    dnn.dnn_net(input_shape=177)
    dnn.train_model(claim_metrics_file, claim_train, claim_label, epoch=150)
    dnn.save_model()
    # 出险率训练集
    claim_train_y, claim_train_yp = dnn.predict(claim_train, claim_label)
    claim_train_error = dnn.cal_error(claim_train_y, claim_train_yp)
    # 出险率验证集
    claim_validate_y, claim_validate_yp = dnn.predict(claim_validate, claim_label)
    claim_validate_error = dnn.cal_error(claim_validate_y, claim_validate_yp)
    dnn.save_result(claim_model_path, claim_validate_y, claim_validate_yp)
    # 出险率测试集
    claim_test_y, claim_test_yp = dnn.predict(claim_test, claim_label)
    claim_test_error = dnn.cal_error(claim_test_y, claim_test_yp)

    with open(claim_metrics_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['训练集', ' '.join(str(i) for i in claim_train_error)])
        writer.writerow(['验证集', ' '.join(str(i) for i in claim_validate_error)])
        writer.writerow(['测试集', ' '.join(str(i) for i in claim_test_error)])

    fmt = '%6.3f' * 3
    print('件均索赔：', '训练集', fmt % claim_train_error,
          '验证集', fmt % claim_validate_error,
          '测试集', fmt % claim_test_error)
