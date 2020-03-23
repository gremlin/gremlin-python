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


class GremlinAPISchedules(GremlinAPI):

    # @classmethod
    # @register_cli_action('list_schedules', ('',), ('teamId',))
    # def list_schedules(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
    #     method = 'GET'
    #     endpoint = cls._optional_team_endpoint(f'/schedules', **kwargs)
    #     payload = cls._payload(**{'headers': https_client.header()})
    #     (resp, body) = https_client.api_call(method, endpoint, **payload)
    #     return body

    @classmethod
    @register_cli_action('create_schedule', ('body',), ('teamId',))
    def create_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_schedule', ('guid',), ('teamId',))
    def get_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('delete_schedule', ('guid',), ('teamId',))
    def delete_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_active_schedules', ('',), ('teamId',))
    def list_active_schedules(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/schedules/active', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_attack_schedules', ('',), ('teamId',))
    def list_attack_schedules(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/schedules/attacks', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('create_attack_schedule', ('body',), ('teamId',))
    def create_attack_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/attacks', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_attack_schedule', ('guid',), ('teamId',))
    def get_attack_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/attacks/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('delete_attack_schedule', ('guid',), ('teamId',))
    def delete_attack_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/attacks/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_scenario_schedules', ('',), ('teamId',))
    def list_scenario_schedules(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('create_scenario_schedule', ('body',), ('teamId',))
    def create_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_scenario_schedule', ('guid',), ('teamId',))
    def get_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_scenario_schedule', ('guid', 'body',), ('teamId',))
    def update_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_param('guid', **kwargs)
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('delete_scenario_schedule', ('guid',), ('teamId',))
    def delete_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('enable_scenario_schedule', ('guid',), ('teamId',))
    def enable_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios/{guid}/enabled', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('disable_scenario_schedule', ('guid',), ('teamId',))
    def disable_scenario_schedule(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/schedules/scenarios/{guid}/enabled', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

