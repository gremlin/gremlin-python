# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

try:
    import requests
    import requests.adapters
except ImportError:
    requests = None

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIHttpClient(object):
    @classmethod
    def api_call(cls, method, uri, headers, params, data, timeout, proxy, verify, max_retries):
        error_message = f'This function is not implemented, please consume the proper http library for your environment'
        log.fatal(error_message)
        raise NotImplementedError(error_message)


class GremlineAPIRequestsClient(GremlinAPIHttpClient):
    @classmethod
    def api_call(cls, method, uri, headers, params, data, timeout, proxy, verify, max_retries):

        request_methods = {
            "HEAD": requests.head,
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch,
        }

        client = request_methods.get(method.upper())


        pass


class GremlinAPIurllibClient(GremlinAPIHttpClient):
    @classmethod
    def api_call(cls, method, uri, headers, params, data, timeout, proxy, verify, max_retries):
        pass


def get_gremlin_httpclient():
    if requests:
        return GremlineAPIRequestsClient
    else:
        return GremlinAPIurllibClient

