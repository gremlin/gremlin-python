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


class GremlinAPIAttacks(object):

    def __init__(self):
        pass

    @classmethod
    def create_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def list_active_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def list_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def list_completed_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def get_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def halt_all_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def halt_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass


