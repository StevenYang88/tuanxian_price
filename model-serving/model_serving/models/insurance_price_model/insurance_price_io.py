#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
input and output class for insurance price model
"""
from model_serving.models.core import SampleFloatScore

INSURANCE_PRICE = "insurance_price"
RISK_RATIO = "keras_risk_ratio"
AVG_CLAIM = "keras_avg_claim"
AVG_PAY = "keras_avg_pay"
AVG_DAYS = "keras_avg_days"


class InsuranceInput(object):
    """
    help class for InsurancePriceModel
    """

    def __init__(self):
        """
        default values
        """
        self._company_ = ""
        self._policy_ = ""
        self._coverage_ = 0
        self._industry_ = 0
        self._occupation_ = 0
        self._city_ = ""
        self._num_ = 0
        self._amount_ = 0.0
        self._avg_age_ = 0.0
        self._sex_ratio_ = 0.0

    def set_company(self, company):
        """
        company help
        :param company:string
        """
        if isinstance(company, str):
            self._company_ = company
        else:
            raise ValueError("company is not str")

    def set_policy(self, policy):
        """
        policy help
        :param policy:string
        """
        if isinstance(policy, str):
            self._policy_ = policy
        else:
            raise ValueError("policy is not str")

    def set_city(self, city):
        """
        city help
        :param city: string
        """
        if isinstance(city, str):
            self._city_ = city
        else:
            raise ValueError("city is not str")

    def set_amount(self, amount):
        """
        amount help
        :param amount:float
        """
        if isinstance(amount, float):
            self._amount_ = amount
        else:
            raise ValueError("amount is not float")

    def set_avg_age(self, avg_age):
        """
        avg_age help
        :param avg_age:float
        """
        if isinstance(avg_age, float):
            self._avg_age_ = avg_age
        else:
            raise ValueError("avg_age is not float")

    def set_sex_ratio(self, sex_ratio):
        """
        sex_ratio help
        :param sex_ratio:
        """
        if isinstance(sex_ratio, float):
            self._sex_ratio_ = sex_ratio
        else:
            raise ValueError("sex_ratio is not float")

    def set_coverage(self, coverage):
        """
        coverage help
        :param coverage:int
        """
        if isinstance(coverage, int):
            self._coverage_ = coverage
        else:
            raise ValueError("coverage is not int")

    def set_industry(self, industry):
        """
        industry int
        :param industry:int
        """
        if isinstance(industry, int):
            self._industry_ = industry
        else:
            raise ValueError("industry is not int")

    def set_occupation(self, occupation):
        """
        occupation help
        :param occupation:
        """
        if isinstance(occupation, int):
            self._occupation_ = occupation
        else:
            raise ValueError("occupation is not int")

    def set_num(self, num):
        """
        num help
        :param num:
        """
        if isinstance(num, int):
            self._num_ = num
        else:
            raise ValueError("num is not int")

    def get_company(self):
        """
        company help
        :return:
            company string
        """
        return self._company_

    def get_policy(self):
        """
        policy help
        :return:
            policy string
        """
        return self._policy_

    def get_coverage(self):
        """
        coverage help
        :return:
            coverage int
        """
        return self._coverage_

    def get_industry(self):
        """
        industry help
        :return:
            industry int
        """
        return self._industry_

    def get_occupation(self):
        """
        occupation help
        :return:
            occupation int
        """
        return self._occupation_

    def get_city(self):
        """
        city help
        :return:
            city string
        """
        return self._city_

    def get_num(self):
        """
        num help
        :return:
            num int
        """
        return self._num_

    def get_amount(self):
        """
        amount help
        :return:
            amount float
        """
        return self._amount_

    def get_avg_age(self):
        """
        avg_age help
        :return:
            avg_age float
        """
        return self._avg_age_

    def get_sex_ratio(self):
        """
        sex_ratio help
        :return:
            sex_ratio float
        """
        return self._sex_ratio_


class InsuranceScore(object):
    """
    InsuranceScore for InsuranceModel
    """

    def __init__(self):
        """
        default values
        """
        self._avg_claim_ = SampleFloatScore()
        self._avg_days_ = SampleFloatScore()
        self._avg_pay_ = SampleFloatScore()
        self._risk_ratio_ = SampleFloatScore()

    def set_avg_claim(self, score):
        """

        :param score: int
        """
        if isinstance(score, SampleFloatScore):
            self._avg_claim_ = score
        else:
            raise ValueError("TypeError", type(score), " is not SampleFloatScore")

    def set_avg_days(self, score):
        """
        :param score:int
        """
        if isinstance(score, SampleFloatScore):
            self._avg_days_ = score
        else:
            raise ValueError("TypeError", type(score), " is not SampleFloatScore")

    def set_avg_pay(self, score):
        """
        :param score:int
        """
        if isinstance(score, SampleFloatScore):
            self._avg_pay_ = score
        else:
            raise ValueError("TypeError", type(score), " is not SampleFloatScore")

    def set_risk_ratio(self, score):
        """
        :param score:float
        """
        if isinstance(score, SampleFloatScore):
            self._risk_ratio_ = score
        else:
            raise ValueError("TypeError", type(score), " is not SampleFloatScore")

    def get_avg_claim(self):
        """
        :return:int
        """
        return self._avg_claim_.get()

    def get_avg_days(self):
        """
        :return:int
        """
        return self._avg_days_.get()

    def get_avg_pay(self):
        """
        :return:int
        """
        return self._avg_pay_.get()

    def get_risk_ratio(self):
        """
        :return:float
        """
        return self._risk_ratio_.get()
