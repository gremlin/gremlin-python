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


class GremlinAPIScenarios(GremlinAPI):

    @classmethod
    @register_cli_action('list_scenarios', ('',), ('teamId',))
    def list_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint('/scenarios', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('create_scenario', ('body',), ('teamId',))
    def create_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_body(**kwargs)
        endpoint = cls._optional_team_endpoint('/scenarios', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_scenario', ('guid',), ('teamId',))
    def get_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_guid(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_scenario', ('guid', 'body'), ('teamId',))
    def update_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PUT'
        guid = cls._error_if_not_guid(**kwargs)
        data = cls._error_if_not_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('archive_scenario', ('guid',), ('teamId',))
    def archive_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_guid(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/archive', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('restore_scenario', ('guid',), ('teamId',))
    def restore_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_guid(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/restore', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_scenario_runs', ('guid',), ('startDate', 'endDate', 'teamId',))
    def list_scenario_runs(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_guid(**kwargs)
        timeset = ''
        start = kwargs.get('startDate', None)
        end = kwargs.get('endDate', None)
        if start:
            timeset += f'startDate={start}&'
        if end:
            timeset += f'endDate={end}'
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs/?{timeset}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('run_scenario', ('guid',), ('teamId', 'body',))
    def run_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_guid(**kwargs)
        data = cls._warn_if_not_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIScenariosRecommended(GremlinAPI):
    pass