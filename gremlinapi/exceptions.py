# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

class GremlinAPIException(Exception):
    """
    Base exception class
    """

class ProxyError(GremlinAPIException):
    """
    Proxy related errors
    """
    def __init__(self, **kwargs):
        message = f'Error for {kwargs["method"]}, please verify proxy configuration'
        super(ProxyError, self).__init__(message)

class ClientError(GremlinAPIException):
    def __init__(self, **kwargs):
        message = f'Error for {kwargs["method"]}, please check your network configuration'
        super(ClientError, self).__init__(message)

