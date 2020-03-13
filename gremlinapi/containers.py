# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.cli import register_cli_action
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIContainers(object):

    @classmethod
    @register_cli_action('list_containers', ('',), ('teamId'))
    def list_containers(cls, http_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/containers'
        method = 'GET'
        headers = http_client.header()
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += f'/?teamId={team_id}'
        (resp, body) = http_client.api_call(method, endpoint, **{'headers': headers})
        return body

