# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.config import GremlinAPIConfig
from gremlinapi.exceptions import (
    GremlinParameterError,
    GremlinAuthError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPISaml(GremlinAPI):
    @classmethod
    def acs(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = '/users/auth/saml/acs'
        data = {
            'SAMLResponse': cls._error_if_not_param('SAMLResponse', **kwargs),
            'RelayState': cls._error_if_not_param('RelayState', **kwargs)
        }
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('samllogin', ('companyName', 'destination', 'acsHandler'), ('',))
    def samllogin(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        params = ['companyName', 'destination', 'acsHandler']
        method = 'GET'
        endpoint = cls._build_query_string_endpoint('/users/auth/saml/login', params, **kwargs)
        payload = cls._payload(**{})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('metadata', ('',), ('',))
    def metadata(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/users/auth/saml/metadata'
        payload = cls._payload(**{})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def sessions(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = '/users/auth/saml/sessions'
        data = {
            'code': cls._error_if_not_param('code', **kwargs)
        }
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
