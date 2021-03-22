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
    HTTPError,
)

from typing import Type

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient, GremlinAPIHttpClient


log = logging.getLogger("GremlinAPI.client")


class GremlinAPIExecutions(GremlinAPI):
    @classmethod
    def _optional_taskid_endpoint(cls, endpoint, **kwargs) -> str:
        task_id: str = cls._info_if_not_param("taskId", **kwargs)
        if task_id:
            endpoint += f"/?taskId={task_id}"
        return cls._optional_team_endpoint(endpoint, **kwargs)

    @classmethod
    @register_cli_action("list_executions", ("",), ("taskId", "teamId"))
    def list_executions(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_taskid_endpoint("/executions", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
