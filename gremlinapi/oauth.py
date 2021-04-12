# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

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


class GremlinAPIOAUTH(GremlinAPI):
    @classmethod
    def configure(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> Union[HTTPResponse, Any]:
        """
        When configuring an OAuth provider we require the following information:
        * `companyId`: Defines the Company ID for OAUTH.
        * `Authoriztion URI`: Used to authenticate against the OAuth provider. We will redirect
            the user to this URL when they initate a OAuth login.
        * `Token URI`: Used to exchange an OAuth code, obtained after logging into the OAuth
            provider, for an access token.
        * `User Info URI`: Used to query for the email of the user..
        * `Client Id`: The public identifier obtained when registering Gremlin with your OAuth
            provider.
        * `Client Secret`: The secret obtained when registering Gremlin with your OAuth provider.
        * `Scope (optional)`: Define what level of access the access token will have that Gremlin
            obtains during the OAuth login. The default is `email`. If you change it from the
            default, the scope provided <strong>must</strong> be able to read the email of
            the user.
        """
        method: str = "POST"
        endpoint: str = (
            "https://api.gremlin.com/v1/companies/%s/oauth/settings"
            % cls._error_if_not_param("companyId", **kwargs)
        )
        data: dict = {
            "authorizationUri": cls._error_if_not_param("authorizationUri", **kwargs),
            "tokenUri": cls._error_if_not_param("tokenUri", **kwargs),
            "userInfoUri": cls._error_if_not_param("userInfoUri", **kwargs),
            "clientId": cls._error_if_not_param("clientId", **kwargs),
            "clientSecret": cls._error_if_not_param("clientSecret", **kwargs),
            "scope": cls._error_if_not_param("scope", **kwargs),
        }
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return resp
