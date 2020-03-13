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


class GremlinAPIExecutions(object):

    @classmethod
    @register_cli_action('list_executions', ('',), ('taskId', 'teamId'))
    def list_executions(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/executions'
        method = 'GET'
        task_id = kwargs.get('taskId', None)
        team_id = kwargs.get('teamId', None)
        if task_id or team_id:
            endpoint += '/?'
            if task_id:
                endpoint += f'taskId={task_id}&'
            if team_id:
                endpoint += f'teamId={team_id}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

