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


class GremlinAPIKubernetesAttacks(GremlinAPI):

    @classmethod
    @register_cli_action('list_all_kubernetes_attacks', ('',), ('teamId'))
    def list_all_kubernetes_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint('/kubernetes/attacks', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('get_kubernetes_attack', ('guid',), ('teamId'))
    def get_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_guid(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/kubernetes/attacks/{guid}', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_kubernetes_attack', ('guid',), ('teamId',))
    def halt_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = cls._error_if_not_guid(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/kubernetes/attacks/{guid}/halt', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_all_kubernetes_attacks', ('',), ('teamId',))
    def halt_all_kubernetes_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = cls._optional_team_endpoint('/kubernetes/attacks/halt', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('new_kubernetes_attack', ('body',), ('teamId'))
    def new_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_body(**kwargs)
        endpoint = cls._optional_team_endpoint('/kubernetes/attacks/new', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body


class GremlinAPIKubernetesTargets(GremlinAPI):

    @classmethod
    @register_cli_action('list_kubernetes_targets', ('',), ('teamId',))
    def list_kubernetes_targets(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint('/kubernetes/targets', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body

