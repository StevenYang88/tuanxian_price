#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
process for InsurancePriceModel
"""
import math
import numpy as np

from sklearn.preprocessing import StandardScaler

from model_serving.models.core import SampleInput
from model_serving.models.core import SampleVector
from model_serving.models.insurance_price_model.insurance_price_io import InsuranceInput


def _classify_age(avg_age):
    """
    classify the avg_age
    :param avg_age: avg_age
    :return: age stage
    """
    avg_age_list = [0, 19, 36, 46, 56, 61, 66]
    for stage, value in enumerate(avg_age_list):
        if float(avg_age) < value:
            return stage
    return len(avg_age_list)


def pre_process(insurance_input):
    """

    :param insurance_input: InsuranceInput
    :return: SampleInput
    """
    if not isinstance(insurance_input, InsuranceInput):
        raise ValueError("insurance_input is not InsuranceInput")
    features = []
    weights = []
    insurance_input.avg_age = _classify_age(insurance_input.avg_age)
    feature_cat = ['policy', 'coverage', 'industry', 'occupation', 'city', 'avg_age']

    for item in feature_cat:
        item_value = insurance_input.__dict__[item]
        features.append(item + '_' + str(item_value))
        weights.append(1.0)

    return SampleInput(features, weights)


def post_process(insurance_input, sample_vector):
    """

    :param insurance_input: InsuranceInput
    :param sample_vector: SampleVector
    :return: SampleVector
    """
    if not isinstance(insurance_input, InsuranceInput):
        raise ValueError("sample_input is not SampleInput")
    if not isinstance(sample_vector, SampleVector):
        raise ValueError("sample_vector is not SampleVector")

    feature_con = ['amount', 'num', 'sex_ratio']
    feature_log = ['amount', 'num']
    others = []

    for item in feature_con:
        if item in feature_log:
            other = math.log10(insurance_input.__dict__[item])
        else:
            other = insurance_input.__dict__[item]
        others.append(other)

    scaler = StandardScaler()
    # scaler.mean_ = np.array([6.19479067, 1.675198, 0.66043834])
    # scaler.scale_ = np.array([0.7849499, 0.52186272, 0.26229562])
    scaler.mean_ = np.array([6.193721, 1.675647, 0.66060])
    scaler.scale_ = np.array([0.785466, 0.522194, 0.26211])
    others = scaler.transform(np.array(others).reshape(1, -1)).reshape(3)
    sample_vector.values += list(others)
    return sample_vector

