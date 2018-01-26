#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
metrics manager
"""
import os
import threading

import psutil

from model_serving.metrics.metric import Metric

# CPU and memory metric are collected every 5 seconds
intervalSec = 5


def cpu(metric_instance):
    """
    CPU
    :param metric_instance:
    :return:
    """
    cpu_usage = psutil.cpu_percent() / 100.0
    metric_instance.update(cpu_usage)

    timer = threading.Timer(intervalSec, cpu, [metric_instance])
    timer.daemon = True
    timer.start()


def memory(metric_instance):
    """
    memory
    :param metric_instance:
    :return:
    """
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_percent() / 100.0
    metric_instance.update(memory_usage)

    timer = threading.Timer(intervalSec, memory, [metric_instance])
    timer.daemon = True
    timer.start()


def disk(metric_instance):
    """
    disk
    :param metric_instance:
    :return:
    """
    disk_usage = psutil.disk_usage('/').percent / 100.0
    metric_instance.update(disk_usage)

    timer = threading.Timer(intervalSec, disk, [metric_instance])
    timer.daemon = True
    timer.start()


class MetricsManager(object):
    """
    Metrics Manager
    """
    metrics = {}

    @staticmethod
    def start(metrics_write_to, mutex):
        """Start service routing.

        Parameters
        ----------
        metrics_write_to : str
            Where metrics will be written to. (log, csv)
        mutex: object
            Mutex to prevent double thread writing on same resource
        """
        MetricsManager.metrics['error_metric'] = \
            Metric('errors', mutex,
                   aggregate_method='interval_sum',
                   write_to=metrics_write_to)
        MetricsManager.metrics['request_metric'] =\
            Metric('requests', mutex,
                   aggregate_method='interval_sum',
                   write_to=metrics_write_to)
        MetricsManager.metrics['cpu_metric'] = \
            Metric('cpu', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to,
                   update_func=cpu)
        MetricsManager.metrics['memory_metric'] = \
            Metric('memory', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to,
                   update_func=memory)
        MetricsManager.metrics['disk_metric'] = \
            Metric('disk', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to,
                   update_func=disk)
        MetricsManager.metrics['overall_latency_metric'] =\
            Metric('overall_latency', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to)
        MetricsManager.metrics['inference_latency_metric'] = \
            Metric('inference_latency', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to)
        MetricsManager.metrics['pre_latency_metric'] = \
            Metric('preprocess_latency', mutex,
                   aggregate_method='interval_average',
                   write_to=metrics_write_to)
