#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Table for convert inputs
id
index
group
group id
group index
debug_doc
"""
import os

from google.protobuf import json_format

from model_serving.models.core import SampleInput
from model_serving.models.core import SampleVector
from model_serving.models.name import FORMAT_TABLE
from model_serving.proto.model_info_pb2 import FormatTable


class Table(object):
    """
    table for features
    """

    def __init__(self, table_path):
        """
        :param table_path:should ends with format_table.json
        """
        format_table = FormatTable()
        if not os.path.exists(table_path):
            raise ValueError("[Table] %s do not exist" % table_path)
        if not table_path.endswith(FORMAT_TABLE):
            raise ValueError("[Table] bad table path %s" % table_path)
        with open(table_path,encoding='utf-8') as f:
            json_format.Parse(f.read(), format_table)
        self.size = format_table.size
        self._id_to_index_ = dict()
        self._index_to_id_ = dict()
        self._id_to_debug_doc_ = dict()
        self._index_to_debug_doc_ = dict()
        for ele in format_table.values:
            if ele.index > self.size:
                raise ValueError("ele.index : %r > self.size : %r" % (ele.index, self.size))
            self._id_to_index_[ele.id] = ele.index
            self._index_to_id_[ele.index] = ele.id
            self._id_to_debug_doc_[ele.id] = ele.debug_doc
            self._index_to_debug_doc_[ele.index] = ele.debug_doc

    def transform(self, sample_input):
        """
        :param sample_input: SampleInput
        :return: SampleVector
        """
        if not isinstance(sample_input, SampleInput):
            raise ValueError("sample_input is not SampleInput")
        vec = [0.0] * self.size
        input_len = len(sample_input.features)
        for i in range(input_len):
            feature_name = sample_input.features[i]
            if feature_name in self._id_to_index_:
                feature_index = self._id_to_index_[feature_name]
                vec[feature_index] = sample_input.weights[i]
            else:
                raise ValueError("feature_name : %r not in table" % feature_name)
        return SampleVector(vec)
