import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.companies import GremlinAPICompanies

from .util import mock_json, mock_data, mock_identifier, hooli_id


class TestCompanies(unittest.TestCase):
    @patch("requests.get")
    def test_get_company_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPICompanies.get_company(**mock_identifier), mock_data)

    @patch("requests.get")
    def test_list_company_clients_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.list_company_clients(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_invite_company_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.invite_company_user(**mock_identifier), mock_data
        )

    @patch("requests.delete")
    def test_delete_company_invite_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.delete_company_invite(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_company_mfa_prefs_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.company_mfa_prefs(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_update_company_prefs_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.update_company_prefs(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_update_company_saml_props_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.update_company_saml_props(**mock_identifier), mock_data
        )

    @patch("requests.get")
    def test_list_company_users_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.list_company_users(**mock_identifier), mock_data
        )

    @patch("requests.put")
    def test_update_company_user_role_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.update_company_user_role(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_activate_company_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.activate_company_user(**mock_identifier), mock_data
        )

    @patch("requests.delete")
    def test_deactivate_company_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.deactivate_company_user(**mock_identifier), mock_data
        )

    @patch("requests.post")
    def test_auth_toggles_with_decorator(self, mock_get) -> None:
        toggles_body = {
            "companyId": hooli_id,
            "passwordEnabled": True,
            "mfaRequired": False,
            "googleEnabled": True,
            "oauthEnabled": True,
            "samlEnabled": True,
            "claimsRequired": False,
        }
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPICompanies.auth_toggles(**toggles_body),
            mock_get.return_value.status_code,
        )
