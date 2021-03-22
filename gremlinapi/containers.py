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


class GremlinAPIContainers(GremlinAPI):
    @classmethod
    @register_cli_action("list_containers", ("",), ("teamId",))
    def list_containers(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/containers", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
