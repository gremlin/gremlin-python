# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.http_clients import get_gremlin_httpclient

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIClients(object):

    def __init__(self):
        pass

    @classmethod
    def activate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def deactivate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def list_active_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def list_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass