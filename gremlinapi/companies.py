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

from typing import Union, Any

log = logging.getLogger("GremlinAPI.client")


class GremlinAPICompanies(GremlinAPI):
    @classmethod
    @register_cli_action("get_company", ("identifier",), ("",))
    def get_company(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        endpoint: str = f"/companies/{identifier}"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_company_clients", ("identifier",), ("",))
    def list_company_clients(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        endpoint: str = f"/companies/{identifier}/clients"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("invite_company_user", ("identifier", "body"), ("",))
    def invite_company_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        data: Union[list, dict] = cls._error_if_not_json_body(**kwargs)
        if isinstance(data, dict):
            data = [dict(data)]
        endpoint: str = f"/companies/{identifier}/invites"
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})  # type: ignore
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("delete_company_invite", ("identifier", "email"), ("",))
    def delete_company_invite(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = f"/companies/{identifier}/invites/{email}"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "company_mfa_prefs",
        ("identifier",),
        (
            "forceMfa",
            "mfaProviders",
            "defaultMfaProvider",
        ),
    )
    def company_mfa_prefs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        data: dict = {
            "forceMfa": cls._info_if_not_param("forceMfa", **kwargs),
            "mfaProviders": cls._info_if_not_param("mfaProviders", **kwargs),
            "defaultMfaProvider": cls._info_if_not_param(
                "defaultMfaProvider", **kwargs
            ),
        }
        data = {k: v for k, v in data.items() if v is not None}
        endpoint: str = f"/companies/{identifier}/mfaPrefs"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("update_company_prefs", ("identifier",), ("domain",))
    def update_company_prefs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        data: dict = {"domain": cls._info_if_not_param("domain", **kwargs)}
        data = {k: v for k, v in data.items() if v is not None}
        endpoint: str = f"/companies/{identifier}/prefs"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "update_company_saml_props",
        ("identifier",),
        ("enabled", "entityId", "idpUrl", "certificate", "forced"),
    )
    def update_company_saml_props(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        data: dict = {
            "enabled": cls._info_if_not_param("enabled", **kwargs),
            "entityId": cls._info_if_not_param("entityId", **kwargs),
            "idpUrl": cls._info_if_not_param("idpUrl", **kwargs),
            "certificate": cls._info_if_not_param("certificate", **kwargs),
            "forced": cls._info_if_not_param("forced", **kwargs),
        }
        data = {k: v for k, v in data.items() if v is not None}
        endpoint: str = f"/companies/{identifier}/saml/props"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_company_users", ("identifier",), ("",))
    def list_company_users(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        endpoint: str = f"/companies/{identifier}/users"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "list_company_users",
        (
            "identifier",
            "email",
        ),
        ("body",),
    )
    def update_company_user_role(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        email: str = cls._error_if_not_email(**kwargs)
        data: Any = cls._warn_if_not_json_body(**kwargs)
        endpoint: str = f"​/companies​/{identifier}​/users​/{email}"
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "activate_company_user",
        (
            "identifier",
            "email",
        ),
        ("",),
    )
    def activate_company_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = f"​/companies​/{identifier}​/users​/{email}​/active"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "deactivate_company_user",
        (
            "identifier",
            "email",
        ),
        ("",),
    )
    def deactivate_company_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = f"​/companies​/{identifier}​/users​/{email}​/active"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def auth_toggles(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> int:
        """
        Authentication Toggles

        Functional arguments toggle Gremlin Authentication settings on or off:

        Argument value must be a `boolean`

        `passwordEnabled` : Is a password required for login
        `mfaRequired` : Is multi factor authentication (mfa) required for login
        `googleEnabled` : Is Google authentication enabled
        `oauthEnabled` : Is OAUTH authentication enabled
        `samlEnabled` : Is SAML authentication enabled
        `claimsRequired` : Are SAML claims required
        """
        method: str = "POST"
        company_id = cls._error_if_not_param("companyId", **kwargs)
        endpoint: str = f"https://api.gremlin.com/v1/companies/{company_id}/auth/prefs"
        data: dict = {
            "passwordEnabled": kwargs.get("passwordEnabled", False),
            "mfaRequired": kwargs.get("mfaRequired", False),
            "googleEnabled": kwargs.get("googleEnabled", False),
            "oauthEnabled": kwargs.get("oauthEnabled", False),
            "samlEnabled": kwargs.get("samlEnabled", False),
            "claimsRequired": kwargs.get("claimsRequired", False),
        }
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return resp.status_code
