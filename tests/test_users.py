import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.users import (
    GremlinAPIUsers,
    GremlinAPIUsersAuth,
    GremlinAPIUsersAuthMFA,
)

from .util import mock_json, mock_data, mock_users, mock_body


class TestUsers(unittest.TestCase):
    # GremlinAPIUsers
    def test__error_if_not_valid_role_statement(self) -> None:
        test_output = GremlinAPIUsers._error_if_not_valid_role_statement(**mock_users)
        self.assertEqual(test_output, mock_users["role"])

    @patch("requests.get")
    def test_list_users_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.list_users(), mock_data)

    @patch("requests.post")
    def test_add_user_to_team_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.add_user_to_team(**mock_body), mock_data)

    @patch("requests.put")
    def test_update_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.update_user(**mock_users), mock_data)

    @patch("requests.delete")
    def test_deactivate_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.deactivate_user(**mock_users), mock_data)

    @patch("requests.get")
    def test_list_active_users_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.list_active_users(), mock_data)

    @patch("requests.post")
    def test_invite_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.invite_user(**mock_users), mock_data)

    @patch("requests.delete")
    def test_revoke_user_invite_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.revoke_user_invite(**mock_users), mock_data)

    @patch("requests.get")
    def test_renew_user_authorization_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIUsers.renew_user_authorization(**mock_users), mock_data
        )

    @patch("requests.get")
    def test_renew_user_authorization_rbac_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIUsers.renew_user_authorization_rbac(**mock_users), mock_data
        )

    @patch("requests.get")
    def test_get_user_self_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.get_user_self(), mock_data)

    @patch("requests.patch")
    def test_update_user_self_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.update_user_self(**mock_body), mock_data)

    @patch("requests.get")
    def test_get_user_session_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsers.get_user_session(), mock_data)

    # GremlinAPIUsersAuth
    @patch("requests.post")
    def test_auth_user_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuth.auth_user(**mock_users), mock_data)

    @patch("requests.post")
    def test_auth_user_sso_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuth.auth_user_sso(**mock_users), mock_data)

    @patch("requests.delete")
    def test_invalidate_session_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuth.invalidate_session(), mock_data)

    @patch("requests.get")
    def test_get_company_affiliations_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIUsersAuth.get_company_affiliations(**mock_users), mock_data
        )

    @patch("requests.get")
    def test_get_saml_metadata_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuth.get_saml_metadata(), mock_data)

    # GremlinAPIUsersAuthMFA
    @patch("requests.post")
    def test_auth_user_mfa_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.auth_user(**mock_users), mock_data)

    @patch("requests.get")
    def test_get_mfa_status_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.get_mfa_status(**mock_users), mock_data)

    @patch("requests.get")
    def test_get_user_mfa_status_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.get_user_mfa_status(), mock_data)

    @patch("requests.post")
    def test_disable_mfa_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.disable_mfa(**mock_users), mock_data)

    @patch("requests.post")
    def test_force_disable_mfa_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIUsersAuthMFA.force_disable_mfa(**mock_users), mock_data
        )

    @patch("requests.post")
    def test_enable_mfa_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.enable_mfa(**mock_users), mock_data)

    @patch("requests.post")
    def test_validate_token_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIUsersAuthMFA.validate_token(**mock_users), mock_data)
