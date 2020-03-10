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

from gremlinapi.cli import register_cli_action
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIAttacks(object):

    def __init__(self):
        pass

    @classmethod
    @register_cli_action('create_attack', ('',), ('',))
    def create_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('list_active_attacks', ('',), ('',))
    def list_active_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('list_attacks', ('',), ('',))
    def list_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('list_complete_attacks', ('',), ('',))
    def list_completed_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('get_attack', ('',), ('',))
    def get_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('halt_all_attacks', ('',), ('',))
    def halt_all_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('halt_attack', ('',), ('',))
    def halt_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass


