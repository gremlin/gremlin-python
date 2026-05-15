# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from datetime import date

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


class GremlinAPIReports(GremlinAPI):
    @classmethod
    @register_cli_action("report_attacks", ("",), ("start", "end", "period", "teamId"))
    def report_attacks(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/attacks", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("report_clients", ("",), ("start", "end", "period", "teamId"))
    def report_clients(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/clients", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "report_companies", ("",), ("start", "end", "period", "teamId")
    )
    def report_companies(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["startDate", "endDate"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/companies", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def report_pricing(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["startDate", "endDate", "trackingPeriod"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/pricing", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("report_teams", ("",), ("start", "end", "period", "teamId", "pageSize"))
    def report_teams(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> list:
        method: str = "GET"
        start_date: str = cls._error_if_not_param("startDate", **kwargs)
        end_date: str = cls._error_if_not_param("endDate", **kwargs)
        page_size = kwargs.get("pageSize", None)
        page_token: str = None
        all_items: list = []
        while True:
            endpoint = cls._add_query_param("/reports/teams/paged", "startDate", start_date)
            endpoint = cls._add_query_param(endpoint, "endDate", end_date)
            endpoint = cls._optional_team_endpoint(endpoint, **kwargs)
            if page_size:
                endpoint = cls._add_query_param(endpoint, "pageSize", str(page_size))
            if page_token:
                endpoint = cls._add_query_param(endpoint, "pageToken", page_token)
            payload: dict = cls._payload(**{"headers": https_client.header()})
            (resp, body) = https_client.api_call(method, endpoint, **payload)
            all_items.extend(body.get("items", []))
            page_token = body.get("pageToken") or None
            if not page_token:
                break
        return all_items

    @classmethod
    @register_cli_action("report_users", ("",), ("start", "end", "period", "teamId"))
    def report_users(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/users", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIReportsSecurity(GremlinAPI):
    @classmethod
    @register_cli_action("report_security_access", ("start", "end"), ("",))
    def report_security_access(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/security/access", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
