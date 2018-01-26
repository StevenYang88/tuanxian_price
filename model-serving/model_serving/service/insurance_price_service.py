#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
InsurancePriceService
"""
import traceback

from google.protobuf import json_format

from model_serving.logger import get_logger
from model_serving.models.insurance_price_model.insurance_price_io import InsuranceInput
from model_serving.models.insurance_price_model.insurance_price_io import InsuranceScore
from model_serving.models.insurance_price_model.insurance_price_model import InsurancePriceModel
from model_serving.proto.model_info_pb2 import InsurancePricePredictionRequest
from model_serving.proto.model_info_pb2 import InsurancePricePredictionResponse
from model_serving.proto.model_info_pb2 import InsurancePriceResponseData
from model_serving.proto.model_info_pb2 import ModelInfo
from model_serving.service.model_service import SingleNodeService

logger = get_logger()


class InsurancePriceService(SingleNodeService):
    """
    InsurancePriceService defines the fundamental loading model and inference
       operations when serving model. This is a base class and needs to be
       inherited.
    """

    def __init__(self, model_info):
        """
        InsurancePriceService
        :param model_info:ModelInfo
        """
        if not isinstance(model_info, ModelInfo):
            raise ValueError("TypeError", type(model_info), "is not ModelInfo")
        self.instance = InsurancePriceModel(model_info.model_path)

    def _inference(self, data):
        """
        step 1 : json string to PredictionRequest,check values
        step 2 : inferance
        step 3 : gen PredictionResponse
        if error occur, return code and error message
        :param data:Json string
        :return:
        """

        prediction_response = InsurancePricePredictionResponse()
        if len(data) == 0:
            prediction_response.code = "BadRequest"
            prediction_response.message = "Input data is empty"
            return prediction_response
        try:
            prediction_request = InsurancePricePredictionRequest()
            json_format.Parse(data, prediction_request)
            insurance_input = self.get_sample_input(prediction_request)
            score = self.instance.inference(insurance_input)
            if not isinstance(score, InsuranceScore):
                raise ValueError("score is not InsuranceScore")
            response_data = InsurancePriceResponseData()
            response_data.risk_ratio = score.get_risk_ratio()
            response_data.avg_claim = score.get_avg_claim()
            response_data.avg_days = score.get_avg_days()
            response_data.avg_pay = score.get_avg_pay()

            prediction_response.response_id = prediction_request.request_id
            prediction_response.data.CopyFrom(response_data)
        except Exception as e:
            prediction_response.code = "BadRequest"
            prediction_response.message = str(e)
            logger.error(traceback.format_exc())

        return json_format.MessageToDict(prediction_response, preserving_proto_field_name=True)

    @staticmethod
    def get_sample_input(request):
        """
        check param
        :param request:
        :return:
        """
        insurance_input = InsuranceInput()
        if len(request.request_id) == 0:
            raise ValueError("request_id is empty")
        insurance_input.request_id = request.request_id
        insurance_input.company = request.company
        insurance_input.policy = request.policy
        if request.coverage < 0:
            raise ValueError("coverage should >= 0")
        insurance_input.coverage = request.coverage
        if request.industry < 0:
            raise ValueError("industry should >= 0")
        insurance_input.industry = request.industry
        if request.occupation < 0:
            raise ValueError("occupation should >= 0")
        insurance_input.occupation = request.occupation
        insurance_input.city = request.city
        insurance_input.num = request.num
        insurance_input.amount = request.amount
        if request.avg_age > 100.0 or request.avg_age < 0:
            raise ValueError("avg_age should be [0,100]")
        insurance_input.avg_age = request.avg_age
        if request.sex_ratio > 1 or request.sex_ratio < 0:
            raise ValueError("sex_ratio should be [0,1]")
        insurance_input.sex_ratio = request.sex_ratio
        return insurance_input
