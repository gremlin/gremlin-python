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

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import (
    get_gremlin_httpclient,
    GremlinAPIHttpClient,
)

from typing import Union, Type

log = logging.getLogger("GremlinAPI.client")


class GremlinAPIMetadata(GremlinAPI):
    @classmethod
    @register_cli_action("get_metadata", ("",), ("teamId",))
    def get_metadata(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/metadata", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
