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
from gremlinapi.scenario_helpers import GremlinScenarioHelper
from gremlinapi.scenario_graph_helpers import GremlinScenarioGraphHelper


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIScenarios(GremlinAPI):
    @classmethod
    def _error_if_not_scenario_body(cls, **kwargs):
        body = cls._error_if_not_param('body', **kwargs)
        if issubclass(type(body), GremlinScenarioHelper) or issubclass(type(body), GremlinScenarioGraphHelper):
            return str(body)
        else:
            error_msg = f'Body present but not of type {type(GremlinScenarioHelper)}'
            log.warning(error_msg)
        return body

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
        data = cls._error_if_not_scenario_body(**kwargs)
        endpoint = cls._optional_team_endpoint('/scenarios', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_scenario', ('guid',), ('teamId',))
    def get_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_scenario', ('guid', 'body'), ('teamId',))
    def update_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PUT'
        guid = cls._error_if_not_param('guid', **kwargs)
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('archive_scenario', ('guid',), ('teamId',))
    def archive_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/archive', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('restore_scenario', ('guid',), ('teamId',))
    def restore_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/restore', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_scenario_runs', ('guid',), ('startDate', 'endDate', 'teamId',))
    def list_scenario_runs(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        timeset = ''
        start = cls._info_if_not_param('startDate', **kwargs)
        end = cls._info_if_not_param('endDate', **kwargs)
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
        guid = cls._error_if_not_param('guid', **kwargs)
        data = cls._warn_if_not_json_body(**kwargs, default=dict())
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_scenario_run_details', ('guid', 'runNumber',), ('teamId',))
    def get_scenario_run_details(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        run_number = cls._error_if_not_param('runNumber', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs/{run_number}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_scenario_result_flags', ('guid', 'runNumber', 'body',), ('teamId',))
    def update_scenario_result_flags(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PUT'
        guid = cls._error_if_not_param('guid', **kwargs)
        run_number = cls._error_if_not_param('runNumber', **kwargs)
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs/{run_number}/resultFlags', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_scenario_result_notes', ('guid', 'runNumber', 'body',), ('teamId',))
    def update_scenario_result_notes(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PUT'
        guid = cls._error_if_not_param('guid', **kwargs)
        run_number = cls._error_if_not_param('runNumber', **kwargs)
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/runs/{run_number}/resultNotes', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_scenario_schedules', ('guid',), ('teamId',))
    def list_scenario_schedules(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/{guid}/schedules', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_active_scenarios', ('',), ('teamId',))
    def list_active_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/scenarios/active', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_archived_scenarios', ('',), ('teamId',))
    def list_archived_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/scenarios/archived', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_draft_scenarios', ('',), ('teamId',))
    def list_draft_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/scenarios/drafts', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('halt_scenario', ('guid', 'runNumber'), ('teamId',))
    def halt_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_param('guid', **kwargs)
        run_number = cls._error_if_not_param('runNumber', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/halt/{guid}/runs/{run_number}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

class GremlinAPIScenariosRecommended(GremlinAPI):

    @classmethod
    @register_cli_action('list_recommended_scenarios', ('',), ('teamId',))
    def list_recommended_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/scenarios/recommended', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_recommended_scenario', ('guid',), ('teamId',))
    def get_recommended_scenario(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/recommended/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_recommended_scenario_static', ('staticEndpointName',), ('teamId',))
    def get_recommended_scenario_static(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        static_endpoint_name = cls._error_if_not_param('staticEndpointName', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/scenarios/recommended/static/{static_endpoint_name}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body