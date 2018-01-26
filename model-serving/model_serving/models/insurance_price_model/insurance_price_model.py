#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
InsurancePriceModel
"""
import os

from model_serving.logger import get_logger
from model_serving.models.format_table import FORMAT_TABLE
from model_serving.models.format_table import Table
from model_serving.models.insurance_price_model.insurance_price_io import AVG_CLAIM
from model_serving.models.insurance_price_model.insurance_price_io import AVG_DAYS
from model_serving.models.insurance_price_model.insurance_price_io import AVG_PAY
from model_serving.models.insurance_price_model.insurance_price_io import INSURANCE_PRICE
from model_serving.models.insurance_price_model.insurance_price_io import InsuranceScore
from model_serving.models.insurance_price_model.insurance_price_io import RISK_RATIO
from model_serving.models.insurance_price_model.insurance_price_process import pre_process
from model_serving.models.insurance_price_model.insurance_price_process import post_process
from model_serving.models.keras_model import KERAS
from model_serving.models.keras_model import KerasModel


logger = get_logger()


class InsurancePriceModel(object):
    """
    InsurancePriceModel
    """

    @staticmethod
    def load_sub_model(model_path, name):
        """
        load sub model
        :param model_path: path for sub model
        :param name:sub model name
        :return: keras model
        """
        m_path = os.path.join(model_path, name)
        if not os.path.exists(m_path):
            raise ValueError("[InsurancePriceModel] %s do not exist" % m_path)
        keras_path = os.path.join(m_path, KERAS)
        return KerasModel(keras_path)

    def __init__(self, model_path):
        """
        Loader
        :param model_path: string
        :return:
        """
        if not os.path.exists(model_path):
            raise ValueError("[InsurancePriceModel] %s do not exist" % model_path)
        if not model_path.endswith(INSURANCE_PRICE):
            raise ValueError("[InsurancePriceModel] bad table path %s" % model_path)
        # table
        table_path = os.path.join(model_path, FORMAT_TABLE)
        self.table = Table(table_path)
        # avg claim
        self.avg_claim = self.load_sub_model(model_path, AVG_CLAIM)
        # avg days
        self.avg_days = self.load_sub_model(model_path, AVG_DAYS)
        # avg pay
        self.avg_pay = self.load_sub_model(model_path, AVG_PAY)
        # risk ratio
        self.risk_ratio = self.load_sub_model(model_path, RISK_RATIO)

    def inference(self, insurance_input):
        """

        :param insurance_input: InsuranceInput
        :return: InsuranceScore
        """
        sample_input = pre_process(insurance_input)
        sample_vector = self.table.transform(sample_input)
        vector = post_process(insurance_input, sample_vector)
        score = InsuranceScore()
        score.set_avg_claim(self.avg_claim.inferance(vector))
        score.set_avg_days(self.avg_days.inferance(vector))
        score.set_avg_pay(self.avg_pay.inferance(vector))
        score.set_risk_ratio(self.risk_ratio.inferance(vector))
        return score
