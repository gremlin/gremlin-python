# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging
import requests
import json

from gremlinapi.util import experimental

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

from typing import Union, Type, Any, Tuple


log = logging.getLogger("GremlinAPI.client")


class GremlinAPIOAUTH(GremlinAPI):
    @classmethod
    @experimental
    def configure(
        cls,
        company_id: str = "",
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> Union[HTTPResponse, Any]:
        """
        Configuration of Gremlin OAUTH

        Arguments:

        `companyId` : Defines the Company ID for OAUTH
        `authorizationUri` : Used to authenticate against the OAuth provider.
            We will redirect the user to this URL when they initate a OAuth login.
        `tokenUri` : Used to exchange an OAuth code.
            This is obtained after logging into the OAuth provider, for an access token.
        `userInfoUri` : Used to query for the email of the user.
        `clientId` : The public identifier obtained when registering Gremlin with your OAuth
            provider.
        `clientSecret` : The secret obtained when registering Gremlin with your OAuth provider.
        `scope` : (OPTIONAL) Define what level of access the access token will have that Gremlin
            obtains during the OAuth login. The default is `email`. If you change it from the
            default, the scope provided must be able to read the email of the user.
        """
        method: str = "POST"
        if not company_id:
            error_msg: str = f"Company ID Required"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

        endpoint: str = (
            f"https://api.gremlin.com/v1/companies/{company_id}/oauth/settings"
        )
        data: dict = {
            "authorizationUri": cls._error_if_not_param("authorizationUri", **kwargs),
            "tokenUri": cls._error_if_not_param("tokenUri", **kwargs),
            "userInfoUri": cls._error_if_not_param("userInfoUri", **kwargs),
            "clientId": cls._error_if_not_param("clientId", **kwargs),
            "clientSecret": cls._error_if_not_param("clientSecret", **kwargs),
            "scope": cls._warn_if_not_param("scope", **kwargs),
        }
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return resp

    @classmethod
    @experimental
    def initiate_oauth(
        cls,
        company_name: str,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
    ) -> Tuple[str, str]:
        """
        Initiates the OAUTH Authentication flow

        Parameters
        ----------
        company_name : str
            The company for which the oauth authentication should commence

        Returns
        ------
        state_cookie, oauth_provider_login_url : Tuple[str, str]

        """
        endpoint: str = (
            f"https://api.gremlin.com/v1/oauth/login?companyName={company_name}"
        )

        # Initiates OAUTH login with Gremlin
        # `allow_redirects` = False enables capture of the response to extract the state cookie
        # `status_code` 307 is a redirect to the OAUTH provider
        login_response = requests.get(endpoint, allow_redirects=False)
        assert login_response.status_code == 307

        state_cookie = login_response.cookies["oauth_state"]
        oauth_provider_login_url = login_response.headers["Location"]
        assert state_cookie != None
        assert oauth_provider_login_url != None

        return state_cookie, oauth_provider_login_url

    @classmethod
    @experimental
    def get_callback_url(
        cls,
        oauth_provider_login_url: str,
        data: dict,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
    ) -> str:
        """
        Retrieves a valid callback url

        Parameters
        ----------
        oauth_provider_login_url : str
            The OAUTH Provider Login URL
        data : dict
            The data dictionary to pass to the OAUTH url.

            `data` is in the following format:
            {
                email: Login email for your user,
                password: Login password for your user,
                state: Value of the state cookie obtained in the previous step,
                redirectUri: URL where your provider should redirect you to after authenticating.
                    It should be https://api.gremlin.com/v1/oauth/callback,
                clientId: Client Id obtained when registering Gremlin with your OAuth provider,
            }

        Returns
        ------
        gremlin_callback_url : str

        """
        # Do not follow redirect as we need to add the state cookie to the next request.
        oauth_provider_login_response = requests.post(
            oauth_provider_login_url, data=data, allow_redirects=False
        )

        # You have now successfully authenticted with your OAuth provider,
        # now continue the flow by following the redirect your OAuth provider
        # created back to Gremlins /oauth/callback endpoint
        log.info(str(oauth_provider_login_response.headers))
        gremlin_callback_url = oauth_provider_login_response.headers["Location"]
        # gremlin_callback_url = auth_body["redirectUri"]
        assert gremlin_callback_url != None
        # NOTE TO SELF: the `location` key is nonexistant on the login_response, and the
        #   redirectUri is `null` in the original state cookie as returned from the mock endpoint
        return gremlin_callback_url

    @classmethod
    @experimental
    def get_access_token(
        cls,
        state_cookie: str,
        gremlin_callback_url: str,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
    ) -> str:
        """
        Retrieves a valid access token to access the next piece of the Gremlin OAUTH flow

        Parameters
        ----------
        state_cookie : str
            The cookie obtained from initiate_oauth()
        gremlin_callback_url : str
            The callback url obtained from get_callback_url()

        Returns
        ------
        access_token : str

        """
        # Add the state cookie to the request and then follow the redirect
        # to Gremlins /oauth/callback endpoint. If the state cookie is not
        # added the request will fail. There is a state parameter in the
        # redirect URL you are following and it needs to match the
        # value in the cookie. This helps prevent CSRF attacks.
        cookie = {"oauth_state": state_cookie}
        gremlin_callback_response = requests.get(gremlin_callback_url, cookies=cookie)
        log.info(str(gremlin_callback_response))
        # The response from the callback endpoint will contain the `access_token` in JSON
        # This is the end of the OAuth specific flow. This `access_token` can
        # now be exchanged for a Gremlin session.
        assert gremlin_callback_response.status_code == 200
        access_token = gremlin_callback_response.json()["access_token"]
        assert access_token != None

        return access_token

    @classmethod
    @experimental
    def get_bearer_token(
        cls,
        company_name: str,
        access_token: str,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
    ) -> str:
        """
        Retrieves a valid bearer token to access the authenticated portions of our API.

        Parameters
        ----------
        company_name : str
            The company for which the bearer token is to generated
        access_token : str
            The access token generated by get_access_token()

        Returns
        ------
        bearer_token : str

        """
        body = {
            "companyName": company_name,
            "accessToken": access_token,
            "provider": "oauth",
        }
        sso_response = requests.post(
            f"https://api.gremlin.com/v1/users/auth/sso?getCompanySession=true",
            data=body,
        )
        assert sso_response.status_code == 200

        # The response is a JSON representation of the session.
        # In this JSON response is the `header` field which contains a
        # Bearer token that can be used in the `Authorization` header
        # when making requests to the Gremlin API.
        bearer_token = sso_response.json()["header"]
        assert bearer_token != None

        return bearer_token

    @classmethod
    @experimental
    def authenticate(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> str:
        """
        Initiates and completes OAUTH authentication

        Parameters
        ----------
        kwargs : dict
            The variables required for OAUTH.

            `kwargs` is required in the following format:
            {
                companyName : The company for which the oauth authentication should commence,
                email: Login email for your user,
                password: Login password for your user,
                clientId: Client Id obtained when registering Gremlin with your OAuth provider,
            }

        Returns
        ------
        bearer_token : str

        """
        company_name = cls._error_if_not_param("companyName", **kwargs)
        (state_cookie, oauth_provider_login_url) = cls.initiate_oauth(
            company_name, https_client
        )
        auth_body = {
            "email": cls._error_if_not_param("email", **kwargs),
            "password": cls._error_if_not_param("password", **kwargs),
            "state": state_cookie,  # obtained in earlier step
            "redirectUri": "https://api.gremlin.com/v1/oauth/callback",
            "clientId": cls._error_if_not_param("clientId", **kwargs),
        }
        gremlin_callback_url = cls.get_callback_url(oauth_provider_login_url, auth_body)
        access_token = cls.get_access_token(state_cookie, gremlin_callback_url)
        bearer_token = cls.get_bearer_token(company_name, access_token)
        return bearer_token
