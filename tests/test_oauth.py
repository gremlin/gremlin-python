import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.oauth import GremlinAPIOAUTH

from .util import mock_json, mock_data, hooli_id


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
            GremlinAPIOAUTH.configure(hooli_id, **config_body), mock_get.return_value
        )

    @patch("requests.get")
    def test_authenticate_with_with(self, mock_get) -> None:
        with patch("requests.post") as mock_post:
            GREMLIN_COMPANY = "Hooli"
            GREMLIN_USER_MOCK = "fakeemail@googlecom"
            GREMLIN_PASSWORD_MOCK = "qwertyuiopoiuytrewq"
            auth_args = {
                "email": GREMLIN_USER_MOCK,
                "password": GREMLIN_PASSWORD_MOCK,
                "clientId": "mocklab_oauth2",
                "companyName": GREMLIN_COMPANY,
            }
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value.json = mock_json
            mock_get.return_value = requests.Response()
            mock_get.return_value.status_code = 307
            mock_get.return_value.json = mock_json
            mock_get.return_value.cookies = {
                "oauth_state": "ewogICJub25jZSIgOiAiZGM2NjA5ODQtNGY2NS00NGYyLWE2MDktODQ0ZjY1ODRmMjM2IiwKICAiY29tcGFueUlkIiA6ICI5Njc2ODY4Yi02MGQyLTVlYmUtYWE2Ni1jMWRlODE2MmZmOWQiLAogICJyZWRpcmVjdFVyaSIgOiBudWxsCn0="
            }
            mock_get.return_value.headers = {
                "Location": "https://api.gremlin.com/v1/oauth/callback",
            }
            self.assertEqual(
                GremlinAPIOAUTH.authenticate(hooli_id, **auth_args),
                mock_post.return_value,
            )

    @patch("requests.post")
    def test_toggles_with_decorator(self, mock_get) -> None:
        toggles_body = {
            "companyId": hooli_id,
            "passwordEnabled": True,
            "mfaRequired": True,
            "googleEnabled": True,
            "oauthEnabled": True,
            "samlEnabled": True,
            "claimsRequired": True,
        }
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOAUTH.toggles(**toggles_body), mock_get.return_value)
