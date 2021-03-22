# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.config import GremlinAPIConfig
from gremlinapi.exceptions import (
    GremlinParameterError,
    GremlinAuthError,
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

from http.client import HTTPResponse

from typing import Union, Type, Any


log = logging.getLogger("GremlinAPI.client")


class GremlinAPISaml(GremlinAPI):
    @classmethod
    def acs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> Union[HTTPResponse, Any]:
        method: str = "POST"
        endpoint: str = "/users/auth/saml/acs"
        data: dict = {
            "SAMLResponse": cls._error_if_not_param("SAMLResponse", **kwargs),
            "RelayState": cls._error_if_not_param("RelayState", **kwargs),
        }
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return resp

    @classmethod
    @register_cli_action(
        "samllogin", ("companyName", "destination", "acsHandler"), ("",)
    )
    def samllogin(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        params: list = ["companyName", "destination", "acsHandler"]
        method: str = "GET"
        endpoint: str = cls._build_query_string_endpoint(
            "/users/auth/saml/login", params, **kwargs
        )
        payload: dict = cls._payload()
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("metadata", ("",), ("",))
    def metadata(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = "/users/auth/saml/metadata"
        payload: dict = cls._payload()
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def sessions(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        endpoint: str = "/users/auth/saml/sessions"
        data: dict = {"code": cls._error_if_not_param("code", **kwargs)}
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
