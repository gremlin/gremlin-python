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
        company_id = cls._error_if_not_param("companyId", **kwargs)
        endpoint: str = f"https://api.gremlin.com/v1/companies/{company_id}/oauth/settings"
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

    def authenticate(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> Union[HTTPResponse, Any]:
        method: str = "POST"
        company_name = cls._error_if_not_param("companyName", **kwargs)
        endpoint: str = f"https://api.gremlin.com/v1/oauth/login?companyName={company_name}"

        # Initiates OAUTH login with Gremlin
        # `allow_redirects` = False enables capture of the response to extract the state cookie
        # `status_code` 307 is a redirect to the OAUTH provider
        login_response = requests.get(endpoint, allow_redirects=False)
        assert login_response.status_code == 307
        
        state_cookie = login_response.cookies['oauth_state']
        oauth_provider_login_url = login_response.headers['Location']
        assert state_cookie != None
        assert oauth_provider_login_url != None

        # The `auth_body` is OAUTH provider specific in terms of the variables it requires
        # - email: Login email for your user
        # - password: Login password for your user
        # - state: Value of the state cookie obtained in the previous step
        # - redirectUri: URL where your provider should redirect you to after authenticating. 
        #                 It should be https://api.gremlin.com/v1/oauth/callback
        # - clientId: Client Id obtained when registering Gremlin with your OAuth provider
        auth_body = {
            'email':  cls._error_if_not_param("email", **kwargs),
            'password': cls._error_if_not_param("password", **kwargs),
            'state': state_cookie, # obtained in earlier step
            'redirectUri': 'https://api.gremlin.com/v1/oauth/callback',
            'clientId': cls._error_if_not_param("clientId", **kwargs)
        }

        # Do not follow redirect as we need to add the state cookie to the next request.
        oauth_provider_login_response = requests.post(
            oauth_provider_login_url, 
            data=auth_body, 
            allow_redirects=False
        )

        # You have now successfully authenticted with your OAuth provider, 
        # now continue the flow by following the redirect your OAuth provider
        # created back to Gremlins /oauth/callback endpoint
        gremlin_callback_url = oauth_provider_login_response.headers['Location']
        assert gremlin_callback_url != None

        # Add the state cookie to the request and then follow the redirect 
        # to Gremlins /oauth/callback endpoint. If the state cookie is not 
        # added the request will fail. There is a state parameter in the 
        # redirect URL you are following and it needs to match the 
        # value in the cookie. This helps prevent CSRF attacks.      
        cookie = {
            'oauth_state': state_cookie
        }
        gremlin_callback_response = requests.get(
            gremlin_callback_url, 
            cookies=cookie
        )

        # The response from the callback endpoint will contain the `access_token` in JSON
        # This is the end of the OAuth specific flow. This `access_token` can 
        # now be exchanged for a Gremlin session.
        assert gremlin_callback_response.status_code == 200
        access_token = gremlin_callback_response.json()['access_token']
        assert access_token != None

        # We now need a valid Gremlin session which can be used to access 
        # the authenticated portions of our API. Craft a request to /users/auth/sso 
        # to exchange access_token for a Gremlin session
        body = {
            'companyName': company_name,
            'accessToken': access_token,
            'provider': 'oauth',
        }
        sso_response = requests.post(
            f"https://api.gremlin.com/v1/users/auth/sso?getCompanySession=true", 
            data=body
        )
        assert sso_response.status_code == 200

        # The response is a JSON representation of the session. 
        # In this JSON response is the `header` field which contains a 
        # Bearer token that can be used in the `Authorization` header 
        # when making requests to the Gremlin API.
        bearer_token = sso_response.json()['header']
        assert bearer_token != None

        return bearer_token