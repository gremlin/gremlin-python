# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
from unittest.mock import patch

# import logging
import requests
from gremlinapi.gremlinapi import GremlinAPI
import gremlinapi.exceptions as g_exceptions

from .util import (
    mock_data,
    mock_team_id,
    mock_body,
    mock_identifier,
    mock_payload,
    hooli_id,
    mock_json,
)

test_param = "myparam"
test_value = "paramval"
test_params = ["myparam", "anotherparam", "team_id"]
test_kwargs = {
    "myparam": "param1val",
    "anotherparam": "param2val",
    "team_id": mock_team_id,
}

test_base_endpoint = "test-endpoint.com"


class TestAPI(unittest.TestCase):
    def test__add_query_param(self) -> None:
        test_endpoint = "%s/?&dummy=yes" % test_base_endpoint
        expected_output = "%s&%s=%s" % (test_endpoint, test_param, test_value)
        self.assertEqual(
            GremlinAPI._add_query_param(test_endpoint, test_param, test_value),
            expected_output,
        )

        test_endpoint = "%s/?&dummy=yes&" % test_base_endpoint
        expected_output = "%s%s=%s" % (test_endpoint, test_param, test_value)
        self.assertEqual(
            GremlinAPI._add_query_param(test_endpoint, test_param, test_value),
            expected_output,
        )

        test_endpoint = "%s" % test_base_endpoint
        expected_output = "%s/?%s=%s" % (test_endpoint, test_param, test_value)
        self.assertEqual(
            GremlinAPI._add_query_param(test_endpoint, test_param, test_value),
            expected_output,
        )

    def test__build_query_string_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = "%s/?%s=%s&%s=%s&%s=%s" % (
            test_endpoint,
            test_params[0],
            test_kwargs[test_params[0]],
            test_params[1],
            test_kwargs[test_params[1]],
            "teamId",
            test_kwargs[test_params[2]],
        )
        self.assertEqual(
            GremlinAPI._build_query_string_endpoint(
                test_endpoint, test_params, **test_kwargs
            ),
            expected_output,
        )

    def test__build_query_string_option_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = "%s/?%s=%s&%s=%s&%s=%s" % (
            test_endpoint,
            test_params[0],
            test_kwargs[test_params[0]],
            test_params[1],
            test_kwargs[test_params[1]],
            "teamId",
            test_kwargs[test_params[2]],
        )
        self.assertEqual(
            GremlinAPI._build_query_string_option_team_endpoint(
                test_endpoint, test_params, **test_kwargs
            ),
            expected_output,
        )

    def test__build_query_string_required_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = "%s/?%s=%s&%s=%s&%s=%s" % (
            test_endpoint,
            test_params[0],
            test_kwargs[test_params[0]],
            test_params[1],
            test_kwargs[test_params[1]],
            "teamId",
            test_kwargs[test_params[2]],
        )
        self.assertEqual(
            GremlinAPI._build_query_string_required_team_endpoint(
                test_endpoint, test_params, **test_kwargs
            ),
            expected_output,
        )

    def test__optional_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint

        expected_output = "%s/?teamId=%s" % (
            test_endpoint,
            test_kwargs[test_params[2]],
        )
        self.assertEqual(
            GremlinAPI._optional_team_endpoint(test_endpoint, **test_kwargs),
            expected_output,
        )

        expected_output = "%s" % (test_endpoint)
        self.assertEqual(
            GremlinAPI._optional_team_endpoint(test_endpoint),
            expected_output,
        )

    def test__required_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint

        try:
            GremlinAPI._required_team_endpoint(test_endpoint)
            self.assertTrue(
                False,
                "Endpoint not provided a team_id but _required_team_endpoint did not throw GremlinParameterError",
            )
        except g_exceptions.GremlinParameterError as gpe:
            self.assertEqual("Endpoint requires a team_id or teamId, none supplied", str(gpe))

    def test__error_if_not_json_body(self) -> None:
        try:
            GremlinAPI._error_if_not_json_body()
            self.assertTrue(False)
        except g_exceptions.GremlinParameterError as gpe:
            self.assertEqual("JSON Body not supplied: {}", str(gpe))

        self.assertEqual(GremlinAPI._error_if_not_json_body(**mock_body), mock_data)

    def test__error_if_not_email(self) -> None:
        try:
            GremlinAPI._error_if_not_json_body()
            self.assertTrue(False)
        except g_exceptions.GremlinParameterError as gpe:
            self.assertEqual("JSON Body not supplied: {}", str(gpe))

        self.assertEqual(
            GremlinAPI._error_if_not_email(**mock_identifier), mock_identifier["email"]
        )

    def test__info_if_not_param(self) -> None:
        test_param = "email"
        self.assertEqual(
            GremlinAPI._info_if_not_param(test_param, **mock_identifier),
            mock_identifier[test_param],
        )
        self.assertEqual(
            GremlinAPI._info_if_not_param("fakeparam", test_param, **mock_identifier),
            test_param,
        )

    def test_payload(self) -> None:
        expected_output = {
            "headers": mock_payload["headers"],
            "body": mock_payload["body"],
            "data": mock_payload["data"],
        }
        self.assertEqual(
            GremlinAPI._payload(**mock_payload),
            expected_output,
        )

    def test__warn_if_not_json_body(self) -> None:
        self.assertEqual(GremlinAPI._warn_if_not_json_body(**mock_body), mock_data)

    def test__warn_if_not_param(self) -> None:
        test_param = "email"
        self.assertEqual(
            GremlinAPI._warn_if_not_param(test_param, **mock_identifier),
            mock_identifier[test_param],
        )
        self.assertEqual(
            GremlinAPI._warn_if_not_param("fakeparam", test_param, **mock_identifier),
            test_param,
        )
