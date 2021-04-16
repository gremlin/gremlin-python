import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.oauth import GremlinAPIOAUTH

from .util import mock_json, mock_data


class TestOAUTH(unittest.TestCase):
    @patch("requests.post")
    def test_configure_with_decorator(self, mock_get) -> None:
        hooli_id = "9676868b-60d2-5ebe-aa66-c1de8162ff9d"
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
