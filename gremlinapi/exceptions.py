# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging


log = logging.getLogger("GremlinAPI.client")


class GremlinAPIException(Exception):
    """
    Base exception class
    """


class APIError(GremlinAPIException):
    def __init__(self, message: str):
        super(APIError, self).__init__(message)


class GremlinAuthError(GremlinAPIException):
    def __init__(self, message: str):
        super(GremlinAuthError, self).__init__(message)


class GremlinIdentifierError(GremlinAPIException):
    def __init__(self, message: str):
        super(GremlinIdentifierError, self).__init__(message)


class GremlinParameterError(GremlinAPIException):
    def __init__(self, message: str):
        super(GremlinParameterError, self).__init__(message)


class GremlinCommandTargetError(GremlinAPIException):
    def __init__(self, message: str):
        super(GremlinCommandTargetError, self).__init__(message)


class ProxyError(GremlinAPIException):
    def __init__(self, uri: str, method: str, **kwargs: dict):
        message: str = f"Error for {method} to {uri}, please verify proxy configuration"
        super(ProxyError, self).__init__(message)


class ClientError(GremlinAPIException):
    def __init__(self, uri: str, method: str, **kwargs: dict):
        message: str = (
            f"Error for {method} to {uri}, please check your network configuration"
        )
        super(ClientError, self).__init__(message)


class HTTPTimeout(GremlinAPIException):
    def __init__(self, uri: str, method: str, timeout: str, **kwargs: dict):
        message: str = f"{method} to {uri} timed out after {timeout}"
        super(HTTPTimeout, self).__init__(message)


class HTTPError(GremlinAPIException):
    def __init__(self, status_code: str = None, reason: str = None):
        message: str = f"Request returned status code {status_code} {reason}"
        super(HTTPError, self).__init__(message)


class HTTPBadHeader(GremlinAPIException):
    def __init__(self, reason: str = None):
        message: str = f"Failed to create HTTPHeader: {reason}"
        super(HTTPBadHeader, self).__init__(message)
