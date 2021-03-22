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


class GremlinAPIHalts(GremlinAPI):
    @classmethod
    @register_cli_action("halt_all_attacks", ("",), ("teamId", "body"))
    def halt_all_attacks(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict
    ) -> dict:
        method: str = "POST"
        data: dict = cls._warn_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint("/halts", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
