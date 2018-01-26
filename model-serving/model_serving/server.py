#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
main function
step 1 : parse args
step 2 : start frontend
step 2.1 : load setting
step 2.2 : start services
step 2.3 : add endpoint
step 2.4 : start handler
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Lock

from model_serving.arg_parser import ArgParser
from model_serving.frontend import ModelServingFrontEnd
from model_serving.logger import LOG_LEVEL_DICT
from model_serving.logger import _Formatter
from model_serving.logger import get_logger
from model_serving.metrics.metrics_manager import MetricsManager

VALID_ROTATE_UNIT = ['S', 'M', 'H', 'D', 'midnight'] + ['W%d' % (i) for i in range(7)]
logger = get_logger()


def _set_root_logger(log_file, log_level, log_rotation_time):
    """Internal function to setup root logger
    """
    assert log_level in LOG_LEVEL_DICT, \
        "log_level must be one of the keys in %s" % (str(LOG_LEVEL_DICT))
    rotate_time_list = log_rotation_time.split(' ')
    assert len(rotate_time_list) > 0 and len(rotate_time_list) < 3, \
        "log_rotation_time must be in format 'interval when' or 'when' for weekday and midnight."
    interval = int(rotate_time_list[0]) if len(rotate_time_list) > 1 else 1
    when = rotate_time_list[-1]
    assert isinstance(interval, int) and interval > 0, "interval must be a positive integer."
    assert when in VALID_ROTATE_UNIT, "rotate time unit must be one of the values in %s." \
                                      % (str(VALID_ROTATE_UNIT))

    root = logging.getLogger()
    root.setLevel(LOG_LEVEL_DICT[log_level])

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_Formatter())
    root.addHandler(stream_handler)

    log_file = log_file or 'log/model_serving.log'
    file_handler = TimedRotatingFileHandler(log_file, when, interval)
    file_handler.setFormatter(_Formatter(colored=False))
    root.addHandler(file_handler)


class ModelServing(object):
    """
    Model Serving
    """

    def __init__(self, app_name='model_serving', args=None):
        """

        """
        # Initialize serving frontend and arg parser
        try:
            parser = ArgParser.model_serving_parser()
            self.args = parser.parse_args(args) if args else parser.parse_args()
            self.threaded = self.args.threaded or False
            self.conf = self.args.conf or "conf/model-serving.json"
            self.frontend = ModelServingFrontEnd(app_name, self.conf)

            # Setup root logger handler and level.
            log_file = self.args.log_file
            log_level = self.args.log_level or "INFO"
            log_rotation_time = self.args.log_rotation_time or "1 H"
            _set_root_logger(log_file, log_level, log_rotation_time)

            logger.info('Initialized model serving.')
        except Exception as e:
            print('Failed to initialize model serving: ' + str(e))
            exit(1)

    def start_model_serving(self):
        """Start model serving server
        """
        try:
            # Process arguments
            self._arg_process()

            # Start model serving host
            self.frontend.start_frontend(self.host, self.port, self.threaded)
            logger.info('Service started successfully.')
            logger.info('Service health endpoint: ' + self.host + ':' + str(self.port) + '/ping')

        except Exception as e:
            logger.error('Failed to start model serving host: ' + str(e))
            exit(1)

    def _arg_process(self):
        """Process arguments before starting service or create application.
        """
        try:
            # Port
            self.port = self.args.port or 8080
            self.host = self.args.host or '127.0.0.1'
            MetricsManager.start(self.args.metrics_write_to, Lock())

        except Exception as e:
            logger.error('Failed to process arguments: ' + str(e))
            exit(1)


def start_serving(app_name='model_serving', args=None):
    """Start service routing.

    Parameters
    ----------
    app_name : str
        App name to initialize model serving.
    args : List of str
        Arguments for starting service. By default it is None
        and commandline arguments will be used. It should follow
        the format recognized by python argparse parse_args method:
        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args.
        An example for model serving arguments:
        """
    model_serving_app = ModelServing(app_name, args=args)
    model_serving_app.start_model_serving()


if __name__ == '__main__':
    start_serving()
