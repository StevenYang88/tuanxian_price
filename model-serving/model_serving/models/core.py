#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
core class for models
input and outputs
"""


class SampleInput(object):
    """
    features : feature name
    weights : feature weight
    sparse feature vector
    """

    def __init__(self, features, weights):
        """

        :param features: list string
        :param weights: list float
        """
        if not len(features) == len(weights):
            raise ValueError("length of feature not equal to length of weights")
        self.features = features
        self.weights = weights


class SampleVector(object):
    """
    DenseVector
    """

    def __init__(self, values):
        """

        :param values: list float
        """
        self.values = values


class SampleFloatScore(object):
    """
    sample float score
    """

    def __init__(self):
        """
        default float score
        """
        self._score_ = 0.0

    def set(self, s):
        """
        :param s: float
        """
        if isinstance(s, float):
            self._score_ = s
        else:
            raise ValueError("TypeError", type(s), " is not float")

    def get(self):
        """
        :return: score float
        """
        return self._score_
