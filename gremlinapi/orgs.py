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


class GremlinAPIOrgs(object):

    def __init__(self):
        pass

    @classmethod
    def list_orgs(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def get_org(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

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

