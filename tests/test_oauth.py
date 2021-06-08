import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.oauth import GremlinAPIOAUTH

from .util import (
    mock_json,
    mock_data,
    hooli_id,
    access_token_json,
    mock_access_token,
    mock_bearer_token,
    bearer_token_json,
)


class TestOAUTH(unittest.TestCase):
    @patch("requests.post")
    def test_configure_with_decorator(self, mock_get) -> None:
        config_body = {
            "authorizationUri": "https://oauth.mocklab.io/oauth/authorize",
            "tokenUri": "https://oauth.mocklab.io/oauth/token",
            "userInfoUri": "https://oauth.mocklab.io/userinfo",
            "clientId": "mocklab_oauth2",
            "clientSecret": "foo",
            "scope": "email",
        }
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIOAUTH.configure(hooli_id, **config_body),
            mock_get.return_value.status_code,
        )

    @patch("requests.get")
    def test_initiate_oauth_with_decorator(self, mock_get) -> None:
        company_name = "Mock Company"
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 307
        mock_get.return_value.json = mock_json
        mock_get.return_value.cookies = {"oauth_state": "mock_oauth_state="}
        mock_get.return_value.headers = {
            "Location": "mock_uri",
        }
        state_cookie, oauth_provider_login_url = GremlinAPIOAUTH.initiate_oauth(
            company_name
        )
        self.assertEqual(
            state_cookie,
            mock_get.return_value.cookies["oauth_state"],
        )
        self.assertEqual(
            oauth_provider_login_url,
            mock_get.return_value.headers["Location"],
        )

    @patch("requests.post")
    def test_get_callback_url_with_decorator(self, mock_post) -> None:
        mock_login_uri = "http://example.com/login"
        mock_callback_uri = "http:example.com/callback"
        auth_body = {
            "email": "mock@email.com",
            "password": "m0ckp44sw0rd",
            "state": "mockstatecookie1234",  # obtained in earlier step
            "redirectUri": "mockredirect.uri.com",
            "clientId": "mock_client_id",
        }
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json
        mock_post.return_value.headers = {
            "Location": mock_callback_uri,
        }
        self.assertEqual(
            GremlinAPIOAUTH.get_callback_url(mock_login_uri, auth_body),
            mock_callback_uri,
        )

    @patch("requests.get")
    def test_get_access_token_with_decorator(self, mock_get) -> None:
        mock_callback_uri = "http:example.com/callback"
        mock_state_cookie = "abd3bd14bvd1beb1eabc1bead1badffcb6af1c6bfd6bddcdca6ddc="
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = access_token_json
        self.assertEqual(
            GremlinAPIOAUTH.get_access_token(mock_state_cookie, mock_callback_uri),
            mock_access_token,
        )

    @patch("requests.post")
    def test_get_bearer_token_with_decorator(self, mock_get) -> None:
        mock_company_name = "Mock Company, Inc."
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = bearer_token_json
        self.assertEqual(
            GremlinAPIOAUTH.get_bearer_token(mock_company_name, mock_access_token),
            mock_bearer_token,
        )
