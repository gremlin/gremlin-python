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


class GremlinAPIContainers(GremlinAPI):

    @classmethod
    @register_cli_action('list_containers', ('',), ('teamId'))
    def list_containers(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/containers'
        method = 'GET'
        headers = https_client.header()
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

