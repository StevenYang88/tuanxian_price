#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
ModelServingFrontEnd
service handler
step 1 : get post body
step 2 : inferance
step 3 : gen json response
"""
from model_serving.handler.flask_handler import FlaskRequestHandler
from model_serving.proto.model_info_pb2 import insurance_price
from model_serving.service.insurance_price_service import InsurancePriceService
from model_serving.setting import Setting


class ModelServingFrontEnd(object):
    """
    ModelServingFrontEnd
    """

    def __init__(self, app_name, conf_path):
        """

        :param app_name:
        :param conf_path:
        """
        self.handler = FlaskRequestHandler(app_name)
        self.setting = Setting(conf_path)
        self.insurance_price_service = \
            InsurancePriceService(self.setting.get_model_info(insurance_price))
        self.handler.add_endpoint("ping", "/ping", self.ping_callback, ["GET"])
        self.handler.add_endpoint("insurance_price",
                                  "/insurance/price",
                                  self.insurance_price_callback,
                                  ["POST"])

    def ping_callback(self):
        """
        Ping Callback
        :return:
        """
        return self.handler.jsonify({"status": "OK"})

    def insurance_price_callback(self):
        """
        InsurancePriceCallback
        step 1 : get post body
        step 2 : inferance
        step 3 : gen json response
        """
        data = self.handler.get_post_body()
        response = self.insurance_price_service.inference(data)
        return self.handler.jsonify(response)

    def start_frontend(self, host, port, threaded):
        """

        :param host:default host
        :param port:default port
        :param threaded:default False
        :return:
        """
        self.handler.start_handler(host, port, threaded)
