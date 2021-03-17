import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.executions import GremlinAPIExecutions

from .util import mock_json, mock_data


class TestExecutions(unittest.TestCase):
    def test__optional_taskid_endpoint(self) -> None:
        test_endpoint = "test-endpoint.com"
        test_kwargs = {"taskId": "134567890"}
        expected_output = "%s/?taskId=%s" % (test_endpoint, test_kwargs["taskId"])
        self.assertEqual(
            GremlinAPIExecutions._optional_taskid_endpoint(
                test_endpoint, **test_kwargs
            ),
            expected_output,
        )

    @patch("requests.get")
    def test_list_executions_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIExecutions.list_executions(), mock_data)
