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


class GremlinAPIMetrics(GremlinAPI):

    @classmethod
    @register_cli_action('get_attack_metrics', ('attackId',), ('teamId',))
    def get_attack_metrics(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        attack_id = cls._error_if_not_param('attackId', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/metrics/attacks/{attack_id}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_scenario_run_metrics', ('scenarioId', 'scenarioRunNumber'), ('teamId',))
    def get_scenario_run_metrics(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        scenario_id = cls._error_if_not_param('scenarioId', **kwargs)
        scenario_run_number = cls._error_if_not_param('scenarioRunNumber', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/metrics/scenarios/{scenario_id}/runs/{scenario_run_number}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

