# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging



log = logging.getLogger('GremlinAPI.client')



class GremlinAPIException(Exception):
    """
    Base exception class
    """

class ProxyError(GremlinAPIException):
    def __init__(self, uri, method, **kwargs):
        message = f'Error for {method} to {uri}, please verify proxy configuration'
        super(ProxyError, self).__init__(message)

class ClientError(GremlinAPIException):
    def __init__(self, uri, method, **kwargs):
        message = f'Error for {method} to {uri}, please check your network configuration'
        super(ClientError, self).__init__(message)

