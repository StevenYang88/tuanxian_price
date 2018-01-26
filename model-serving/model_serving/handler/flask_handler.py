#!/bin/env python
# -*- coding=utf8 -*-
################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################
"""
FlaskRequestHandler
* start_handler
  * start the handler
* add_endpoint
  * add urls
* get_post_body
  * get post body
* jsonify
  * dict to json
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from model_serving.handler.request_handler import RequestHandler
from model_serving.logger import get_logger

logger = get_logger()


class FlaskRequestHandler(RequestHandler):
    """
    Flask HttpRequestHandler for handling requests.
    """

    def __init__(self, app_name):
        """
        Contructor for Flask request handler.
        
        Parameters
        ----------
        app_name : string 
            App name for handler.
        """
        self.app = Flask(app_name)
        CORS(self.app)

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
        try:
            self.app.run(host=host, port=port, threaded=threaded)
        except Exception as e:
            raise Exception('Flask handler failed to start: ' + str(e))

    def add_endpoint(self, api_name, endpoint, callback, methods):
        """
        Add an endpoint for Flask

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

        # Flask need to be passed with a method list
        try:
            assert isinstance(methods, list), 'methods should be a list: [GET, POST] by Flask.'
            self.app.add_url_rule(endpoint, api_name, callback, methods=methods)
        except Exception as e:
            raise Exception('Flask handler failed to add endpoints: ' + str(e))

    def get_post_body(self):
        """
        Get post body from a request.

        Returns
        ----------
        Object: 
            raw_input_string
        """
        logger.info('Getting json string from request.')
        return request.get_data()

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
        logger.info('Jsonifying the response: ' + str(response))
        return jsonify(response)
