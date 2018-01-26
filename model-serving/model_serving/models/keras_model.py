#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Load Keras Model
"""
import os

import numpy as np
import tensorflow as tf
from keras.models import model_from_json

from model_serving.logger import get_logger
from model_serving.models.core import SampleFloatScore
from model_serving.models.name import KERAS
from model_serving.models.name import KERAS_WEIGHTS
from model_serving.models.name import KERAS_NETWORK

logger = get_logger()


class KerasModel(object):
    """
    keras models
    """

    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise ValueError("[KerasModel] %s do not exist" % model_path)
        if not model_path.endswith(KERAS):
            raise ValueError("bad table path %s" % model_path)

        keras_network_path = os.path.join(model_path, KERAS_NETWORK)
        if not os.path.exists(keras_network_path):
            raise ValueError("[KerasModel] %s do not exist" % keras_network_path)
        logger.debug("[KerasModel] start load network")
        self._instance_ = model_from_json(open(keras_network_path).read())
        logger.debug("[KerasModel] finish load network")

        keras_weights_path = os.path.join(model_path, KERAS_WEIGHTS)
        if not os.path.exists(keras_weights_path):
            raise ValueError("[KerasModel] %s do not exist" % keras_weights_path)
        logger.debug("[KerasModel] start load weights")
        self._instance_.load_weights(keras_weights_path)
        logger.debug("[KerasModel] finish load weights")

        # important !!!
        # important !!!
        # important !!!
        self.graph = tf.get_default_graph()

    def inferance(self, sample_vector):
        """
        :param sample_vector:SampleVector
        :return:SampleScore
        """
        sample_score = SampleFloatScore()
        vector = np.reshape(sample_vector.values, (1, 177))

        # important !!!
        # important !!!
        # important !!!
        with self.graph.as_default():
            score = self._instance_.predict(vector)
            if not np.shape(score) == (1, 1):
                raise ValueError("[KerasModel] ", np.shape(score))
            else:
                sample_score.set(float(score[0, 0]))
                return sample_score
