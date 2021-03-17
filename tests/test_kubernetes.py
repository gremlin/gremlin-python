import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.kubernetes import (
    GremlinAPIKubernetesAttacks,
    GremlinAPIKubernetesTargets,
)

from .util import mock_json, mock_data, mock_uid, mock_body


class TestKubernetesAttacks(unittest.TestCase):
    @patch("requests.get")
    def test_list_all_kubernetes_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesAttacks.list_all_kubernetes_attacks(), mock_data
        )

    @patch("requests.get")
    def test_get_kubernetes_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesAttacks.get_kubernetes_attack(**mock_uid), mock_data
        )

    @patch("requests.post")
    def test_halt_kubernetes_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesAttacks.halt_kubernetes_attack(**mock_uid), mock_data
        )

    @patch("requests.post")
    def test_halt_all_kubernetes_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesAttacks.halt_all_kubernetes_attacks(), mock_data
        )

    @patch("requests.post")
    def test_new_kubernetes_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesAttacks.new_kubernetes_attack(**mock_body), mock_data
        )


class TestKubernetesTargets(unittest.TestCase):
    @patch("requests.get")
    def test_list_kubernetes_targets_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIKubernetesTargets.list_kubernetes_targets(), mock_data
        )
