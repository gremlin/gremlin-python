# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
import requests
import logging
from unittest.mock import patch
from gremlinapi.alfi import GremlinALFI

from .util import mock_json, mock_body, mock_data, mock_guid


class TestAlfi(unittest.TestCase):
    @patch("requests.post")
    def test_create_alfi_experiment_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.create_alfi_experiment(**mock_body), mock_data)

    @patch("requests.delete")
    def test_halt_all_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.halt_all_alfi_experiments(), mock_data)

    @patch("requests.get")
    def test_get_alfi_experiment_details_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinALFI.get_alfi_experiment_details(**mock_guid), mock_data
        )

    @patch("requests.delete")
    def test_halt_alfi_experiment_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.halt_alfi_experiment(**mock_guid), mock_data)

    @patch("requests.get")
    def test_list_active_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.list_active_alfi_experiments(), mock_data)

    @patch("requests.get")
    def test_list_completed_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.list_completed_alfi_experiments(), mock_data)
