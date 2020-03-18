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
        endpoint = '/kubernetes/attacks'
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('get_kubernetes_attack', ('guid',), ('teamId'))
    def get_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = kwargs.get('guid', None)
        if not guid:
            error_msg = f'Attack GUID not supplied to get_k8_attack: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = f'/kubernetes/attacks/{guid}'
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_kubernetes_attack', ('guid',), ('teamId',))
    def halt_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        guid = kwargs.get('guid', None)
        if not guid:
            error_msg = f'Attack GUID not supplied to get_k8_attack: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = f'/kubernetes/attacks/{guid}/halt'
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_all_kubernetes_attacks', ('',), ('teamId',))
    def halt_all_kubernetes_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = f'/kubernetes/attacks/halt'
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('new_kubernetes_attack', ('body',), ('teamId'))
    def new_kubernetes_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = f'/kubernetes/attacks/new'
        data = kwargs.get('body', None)
        if not data:
            error_msg = f'JSON Attack body not provided: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body


class GremlinAPIKubernetesTargets(GremlinAPI):

    @classmethod
    @register_cli_action('list_kubernetes_targets', ('',), ('teamId',))
    def list_kubernetes_targets(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/kubernetes/targets'
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body

