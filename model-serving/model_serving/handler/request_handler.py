#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
base handler for request
"""
from abc import ABCMeta
from abc import abstractmethod


class RequestHandler(object):
    """
    HttpRequestHandler for handling http requests.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, app_name):
        """
        Contructor for request handler.
        
        Parameters
        ----------
        app_name : string 
            App name for handler.
        """
        pass

    @abstractmethod
    def start_handler(self, host, port, threaded):
        """
        Start request handler.

        Parameters
        ----------
        host : string 
            Host to setup handler.
        port: int
            Port to setup handler.
        threaded: bool
            Threaded to setup handler.
        """
        pass

    @abstractmethod
    def add_endpoint(self, endpoint, api_name, callback, methods):
        """
        Add endpoint for request handler.

        Parameters
        ----------
        endpoint : string 
            Endpoint for handler. 
        api_name: string
            Endpoint ID for handler.

        callback: function
            Callback function for endpoint.

        methods: List
            Http request methods [POST, GET].
        """
        pass

    @abstractmethod
    def get_post_body(self):
        """
        Get json string from a request.
        ----------
           string.
        """
        pass

    @abstractmethod
    def jsonify(self, response):
        """
        Jsonify a response.
        
        Parameters
        ----------
        response : Response 
            response to be jsonified.

        Returns
        ----------
        Response: 
            Jsonified response.
        """
        pass
