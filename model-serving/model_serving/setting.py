#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
settinglib
"""
import os

from google.protobuf import json_format

from model_serving.proto.model_info_pb2 import ModelInfo


class Setting(object):
    """
    Setting from file
    """

    def __init__(self, conf_file):
        """

        :param conf_file:
        """
        if not os.path.exists(conf_file):
            raise ValueError("%s do not exist" % conf_file)
        self.model_info = dict()
        with open(conf_file) as f:
            for line in f:
                info = ModelInfo()
                json_format.Parse(line, info)
                if info.model_type not in self.model_info:
                    self.model_info[info.model_type] = info
                else:
                    raise ValueError("Do not support two models")

    def get_model_info(self, model_type):
        """

        :param model_type:
        :return:list
        """
        if model_type in self.model_info:
            return self.model_info[model_type]
        else:
            return None
