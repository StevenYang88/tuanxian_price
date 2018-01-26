#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Base Model Service
"""
import time
from abc import ABCMeta
from abc import abstractmethod

from model_serving.logger import get_logger
from model_serving.metrics.metrics_manager import MetricsManager

logger = get_logger()


class ModelService(object):
    """
    ModelService wraps up all preprocessing, inference and postprocessing
    functions used by model service. It is defined in a flexible manner to
    be easily extended to support different frameworks.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        default
        """
        pass

    @abstractmethod
    def inference(self, data):
        """
        Wrapper function to run inference and functions.

        Parameters
        ----------
        data : list of object
            Raw input from request.

        Returns
        -------
        list of outputs to be sent back to client.
            data to be sent back
        """
        pass


class SingleNodeService(ModelService):
    """
    SingleNodeModel defines abstraction for model service
    which loads a single model.
    """

    def inference(self, data):
        """
        Wrapper function to run preprocess, inference and postprocess functions.
        """

        infer_start_time = time.time()

        data = self._inference(data)

        # Update inference latency metric
        infer_time_in_ms = (time.time() - infer_start_time) * 1000
        if 'inference_latency_metric' in MetricsManager.metrics:
            MetricsManager.metrics['inference_latency_metric'].update(infer_time_in_ms)
        return data

    @abstractmethod
    def _inference(self, data):
        """
        Internal inference methods. Run forward computation and
        return output.
        """
        return data
