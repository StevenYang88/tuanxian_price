# -*- coding: utf-8 -*-

################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Main function
"""

from timeit import default_timer as timer
from models.avg_claim_model import train_avg_claim
from models.avg_days_model import train_avg_days
from models.avg_pay_model import train_avg_pay
from models.risk_ratio_model import train_risk_ratio


def train_model():
    """

    :return:
    """
    data_path = './data/'
    metrics_path = './metrics/'
    data_type = {'policy': str, 'coverage': str, 'industry': str, 'occupation': str, 'city': str,
                 'log_amount': float, 'log_num': float, 'avg_age': float, 'sex_ratio': float,
                 'risk_ratio': float, 'avg_pay': float, 'avg_claim': float, 'avg_days': float}

    risk_flag = True
    pay_flag = True
    claim_flag = True
    days_flag = True

    start_training = timer()

    if risk_flag:
        train_risk_ratio(data_path, data_type, metrics_path)
    if pay_flag:
        train_avg_pay(data_path, data_type, metrics_path)
    if claim_flag:
        train_avg_claim(data_path, data_type, metrics_path)
    if days_flag:
        train_avg_days(data_path, data_type, metrics_path)

    end_training = timer()
    print('Train_time: ', end_training - start_training)


if __name__ == '__main__':
    train_model()
