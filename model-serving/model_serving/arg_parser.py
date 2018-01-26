#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
Argument
"""
import argparse


class ArgParser(object):
    """
    Argument parser for model-serving
    """

    @staticmethod
    def model_serving_parser():
        """ Argument parser for model serving start service
        """
        parser = argparse.ArgumentParser(prog='model-serving', description='Model Serving')

        parser.add_argument('--port', help='Port number. By default it is 8080.')

        parser.add_argument('--host', help='Host. By default it is localhost.')

        parser.add_argument('--threaded', help='Threaded. By default it is False.')

        parser.add_argument('--conf',
                            help='Conf file name. By default it is conf/model-serving.json')

        parser.add_argument('--log-file',
                            help='Log file name. '
                                 'By default it is "log/model_serving_app.log" '
                                 'in the current folder.')

        parser.add_argument('--log-rotation-time',
                            help='Log rotation time. '
                                 'By default it is "1 H", which means one Hour. '
                                 'Valid format is "interval when", '
                                 'where _when_ can be "S", "M", "H", or "D". '
                                 'For a particular weekday use only "W0" - "W6". '
                                 'For midnight use only "midnight". '
                                 'for detailed information on values.')

        parser.add_argument('--log-level', help='Log level. By default it is INFO.')

        parser.add_argument('--metrics-write-to',
                            default='log',
                            choices=['log', 'csv'],
                            help='By default writes to the Log file specified in `--log-file`.'
                                 'If you pass "csv", various metric files in '
                                 '"csv" format are created in metrics folder '
                                 'in the current directory. ')

        return parser
