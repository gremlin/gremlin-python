# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIOrgs(GremlinAPI):

    def __init__(self):
        pass

    @classmethod
    def list_orgs(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/orgs'
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers':header})
        return body

    @classmethod
    def get_org(cls, https_client=get_gremlin_httpclient(), **kwargs):
        return "get_org"

    @classmethod
    def create_org(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def new_certificate(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def delete_certificate(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def delete_old_certificate(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def reset_secret(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

