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

from typing import Union, Type

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import (
    get_gremlin_httpclient,
    GremlinAPIHttpClient,
)
from gremlinapi.scenario_graph_helpers import GremlinScenarioGraphHelper


log = logging.getLogger("GremlinAPI.client")


class GremlinAPIScenarios(GremlinAPI):
    @classmethod
    def _error_if_not_scenario_body(
        cls,
        **kwargs: dict,
    ) -> str:
        body: GremlinScenarioGraphHelper = cls._error_if_not_param("body", **kwargs)  # type: ignore
        if issubclass(type(body), GremlinScenarioGraphHelper):
            return str(body)
        else:
            error_msg: str = (
                f"Body present but not of type {type(GremlinScenarioGraphHelper)}"
            )
            log.warning(error_msg)
        return str(body)

    @classmethod
    @register_cli_action("list_scenarios", ("",), ("teamId",))
    def list_scenarios(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/scenarios", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("create_scenario", ("body",), ("teamId",))
    def create_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: str = cls._error_if_not_scenario_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint("/scenarios", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})  # type: ignore
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_scenario", ("guid",), ("teamId",))
    def get_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("update_scenario", ("guid", "body"), ("teamId",))
    def update_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("archive_scenario", ("guid",), ("teamId",))
    def archive_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/archive", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("restore_scenario", ("guid",), ("teamId",))
    def restore_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/restore", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "list_scenario_runs",
        ("guid",),
        (
            "startDate",
            "endDate",
            "teamId",
        ),
    )
    def list_scenario_runs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> list:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        start: str = cls._info_if_not_param("startDate", **kwargs)
        end: str = cls._info_if_not_param("endDate", **kwargs)
        limit = kwargs.get("pageSize", 50)
        run_number: str = None
        all_items: list = []
        while True:
            endpoint = cls._optional_team_endpoint(f"/scenarios/{guid}/runs/paged", **kwargs)
            if start:
                endpoint = cls._add_query_param(endpoint, "startDate", start)
            if end:
                endpoint = cls._add_query_param(endpoint, "endDate", end)
            endpoint = cls._add_query_param(endpoint, "limit", str(limit))
            if run_number:
                endpoint = cls._add_query_param(endpoint, "runNumber", run_number)
            payload: dict = cls._payload(**{"headers": https_client.header()})
            log.debug(f"list_scenario_runs: fetching page runNumber={run_number or 1} endpoint={endpoint}")
            (resp, body) = https_client.api_call(method, endpoint, **payload)
            page_items = body.get("items", [])
            all_items.extend(page_items)
            next_run_number = body.get("pageToken") or None
            log.debug(f"list_scenario_runs: got {len(page_items)} items, total={len(all_items)}, next pageToken={next_run_number}")
            if not next_run_number or not page_items or next_run_number == run_number:
                break
            run_number = next_run_number
        return all_items

    @classmethod
    @register_cli_action(
        "list_scenarios_runs",
        (),
        (
            "startDate",
            "endDate",
            "teamId",
        ),
    )
    def list_scenarios_runs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        timeset: str = ""
        state_query: str = ""
        state: str = cls._info_if_not_param("state", **kwargs)
        start: str = cls._info_if_not_param("startDate", **kwargs)
        end: str = cls._info_if_not_param("endDate", **kwargs)
        if start:
            timeset += f"startDate={start}&"
        if end:
            timeset += f"endDate={end}"
        if state:
            state_query += f"&state={state}"
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/runs/?{timeset}{state_query}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "run_scenario",
        ("guid",),
        (
            "teamId",
            "body",
        ),
    )
    def run_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        data: dict = cls._warn_if_not_json_body(**kwargs, default=dict())
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/{guid}/runs", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "get_scenario_run_details",
        (
            "guid",
            "runNumber",
        ),
        ("teamId",),
    )
    def get_scenario_run_details(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        run_number: int = cls._error_if_not_param("runNumber", **kwargs)  # type: ignore
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/runs/{run_number}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "update_scenario_result_flags",
        (
            "guid",
            "runNumber",
            "body",
        ),
        ("teamId",),
    )
    def update_scenario_result_flags(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        run_number: int = cls._error_if_not_param("runNumber", **kwargs)  # type: ignore
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/runs/{run_number}/resultFlags", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "update_scenario_result_notes",
        (
            "guid",
            "runNumber",
            "body",
        ),
        ("teamId",),
    )
    def update_scenario_result_notes(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        run_number: int = cls._error_if_not_param("runNumber", **kwargs)  # type: ignore
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/runs/{run_number}/resultNotes", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        # Content-Type must be text/plain for this endpoint
        payload['headers']['Content-Type'] = 'text/plain'
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_scenario_schedules", ("guid",), ("teamId",))
    def list_scenario_schedules(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/{guid}/schedules", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_active_scenarios", ("",), ("teamId",))
    def list_active_scenarios(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> list:
        method: str = "GET"
        page_size = kwargs.get("pageSize", None)
        page_token: str = None
        all_items: list = []
        while True:
            endpoint = cls._optional_team_endpoint("/scenarios/active/paged", **kwargs)
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
    @register_cli_action("list_archived_scenarios", ("",), ("teamId",))
    def list_archived_scenarios(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/archived", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_draft_scenarios", ("",), ("teamId",))
    def list_draft_scenarios(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/drafts", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("halt_scenario", ("guid", "runNumber"), ("teamId",))
    def halt_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        run_number: int = cls._error_if_not_param("runNumber", **kwargs)  # type: ignore
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/halt/{guid}/runs/{run_number}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIScenariosRecommended(GremlinAPI):
    @classmethod
    @register_cli_action("list_recommended_scenarios", ("",), ("teamId",))
    def list_recommended_scenarios(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/scenarios/recommended", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_recommended_scenario", ("guid",), ("teamId",))
    def get_recommended_scenario(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/recommended/{guid}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "get_recommended_scenario_static", ("staticEndpointName",), ("teamId",)
    )
    def get_recommended_scenario_static(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        static_endpoint_name: str = cls._error_if_not_param(
            "staticEndpointName", **kwargs
        )
        endpoint: str = cls._optional_team_endpoint(
            f"/scenarios/recommended/static/{static_endpoint_name}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
