import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.reliability_tests import GremlinAPIReliabilityTests
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.exceptions import GremlinParameterError
from .util import (
    api_key as mock_api_key,
    mock_team_id,
    mock_json,
    mock_data,
    mock_service_id,
    mock_reliability_test_id,
    mock_dependency_id
)


class TestReliabilityTests(unittest.TestCase):

    old_api_key = None
    old_team_id = None

    def setUp(self) -> None:
        # Store the old keys for restoration after tests
        self.old_api_key = config.api_key
        self.old_team_id = config.team_id

    def tearDown(self) -> None:
        # Restore the old keys in case we changed them
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id


    ###############################
    # list_reliability_test_types()
    #   - Test that the method works with config-based team_id
    #   - Test that the method works with kwarg team_id
    #   - Test that the method raises GremlinParameterError if no team_id is set
    ###############################

    @patch('requests.get')
    def test_list_reliability_test_types_config_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_types method works with config-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        self.assertEqual(
            GremlinAPIReliabilityTests().list_reliability_test_types(),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch('requests.get')
    def test_list_reliability_test_types_kw_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_types method works with kwarg-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIReliabilityTests().list_reliability_test_types(team_id = mock_team_id),
            mock_data
        )

    @patch('requests.get')
    def test_list_reliability_test_types_no_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_types method fails with no team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_reliability_test_types()

    ##############################
    # list_reliability_test_runs()
    #  - Test that the method works with config-based team_id
    #  - Test that the method works with kwarg team_id
    #  - Test that the method raises GremlinParameterError if no team_id is set
    #  - Test that the method raises GremlinParameterError if no service_id is set
    ##############################

    @patch('requests.get')
    def test_list_service_reliability_test_runs_config_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs method works with config-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        self.assertEqual(
            GremlinAPIReliabilityTests().list_service_reliability_test_runs(service_id = mock_service_id),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch('requests.get')
    def test_list_service_reliability_test_runs_kw_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs method works with kwarg-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIReliabilityTests().list_service_reliability_test_runs(team_id = mock_team_id, service_id = mock_service_id),
            mock_data
        )

    @patch('requests.get')
    def test_list_service_reliability_test_runs_no_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs method fails with no team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_service_reliability_test_runs(service_id = mock_service_id)

    @patch('requests.get')
    def test_list_service_reliability_test_runs_no_service_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs method fails with no service_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_service_reliability_test_runs(team_id = mock_team_id)

    #############################################
    #list_service_reliability_test_runs_by_type()
    #  - Test that the method works with config-based team_id
    #  - Test that the method works with kwarg team_id
    #  - Test that the method raises GremlinParameterError if no team_id is set
    #  - Test that the method raises GremlinParameterError if no service_id is set
    #  - Test that the method raises GremlinParameterError if no reliability_test_id is set
    #############################################

    @patch('requests.get')
    def test_list_service_reliability_test_runs_by_type_config_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs_by_type method works with config-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        self.assertEqual(
            GremlinAPIReliabilityTests().list_service_reliability_test_runs_by_type(service_id = mock_service_id, reliability_test_id = mock_reliability_test_id),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch('requests.get')
    def test_list_service_reliability_test_runs_by_type_kw_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs_by_type method works with kwarg-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIReliabilityTests().list_service_reliability_test_runs_by_type(team_id = mock_team_id, service_id = mock_service_id, reliability_test_id = mock_reliability_test_id),
            mock_data
        )

    @patch('requests.get')
    def test_list_service_reliability_test_runs_by_type_no_team_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs_by_type method fails with no team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_service_reliability_test_runs_by_type(service_id = mock_service_id, reliability_test_id = mock_reliability_test_id)

    @patch('requests.get')
    def test_list_service_reliability_test_runs_by_type_no_service_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs_by_type method fails with no service_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_service_reliability_test_runs_by_type(team_id = mock_team_id, reliability_test_id = mock_reliability_test_id)

    @patch('requests.get')
    def test_list_service_reliability_test_runs_by_type_no_reliability_test_id(self,mock_get) -> None:
        '''
        Test that the list_service_reliability_test_runs_by_type method fails with no reliability_test_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_service_reliability_test_runs_by_type(team_id = mock_team_id, service_id = mock_service_id)


    #######################################
    # list_reliability_test_notifications()
    #  - Test that the method works with config-based team_id
    #  - Test that the method works with kwarg team_id
    #  - Test that the method raises GremlinParameterError if no team_id is set
    #######################################

    @patch('requests.get')
    def test_list_reliability_test_notifications_config_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_notifications method works with config-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        self.assertEqual(
            GremlinAPIReliabilityTests().list_reliability_test_notifications(),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch('requests.get')
    def test_list_reliability_test_notifications_kw_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_notifications method works with kwarg-based team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().list_reliability_test_notifications(team_id = mock_team_id),
            mock_data
        )

    @patch('requests.get')
    def test_list_reliability_test_notifications_no_team_id(self,mock_get) -> None:
        '''
        Test that the list_reliability_test_notifications method fails with no team_id
        '''
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().list_reliability_test_notifications()

    ###############################
    # run_single_reliability_test()
    #  - Test that the method works with config-based team_id
    #  - Test that the method works with kwarg team_id
    #  - Test that the method raises GremlinParameterError if no team_id is set
    #  - Test that the method raises GremlinParameterError if no reliability_test_id is set
    #  - Test that the method raises GremlinParameterError if no service_id is set
    #  - Test that the method raises GremlinParameterError if the selected reliability_test_id
    #       required a dependency_id, but none was provided.
    #  - Test that the method works if the selected reliability_test_id requires a dependency_id
    #       and one is provided.
    #  - Test that the method works if the selected reliability_test_id does not require a dependency_id
    #       and none is provided.
    #  - Test that the method raises GremlinParameterError if the selected reliability_test_id does
    #       not require a dependency_id, but one is provided.
    ###############################

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_config_team_id(self,mock_post,mock_validate) -> None:
        '''
        Test that the run_single_reliability_test method works with config-based team_id
        Need to patch out __validate_reliability_test_id because it's called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        self.assertEqual(
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
            ),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_kw_team_id(self,mock_post,mock_validate) -> None:
        '''
        Test that the run_single_reliability_test method works with kwarg-based team_id
        Need to patch out __validate_reliability_test_id because it's called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().run_single_reliability_test(
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
                team_id = mock_team_id,
            ),
            mock_data
        )

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_no_team_id(self,mock_post,mock_validate) -> None:
        '''
        Test that the run_single_reliability_test method fails with no team_id
        Need to patch out __validate_reliability_test_id because it's called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_single_reliability_test(
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
            )

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_no_reliability_test_id(self,mock_post,mock_validate) -> None:
        '''
        Test that the run_single_reliability_test method fails with no reliability_test_id
        Need to patch out __validate_reliability_test_id because it's called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                service_id = mock_service_id,
            )
    
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_no_service_id(self,mock_post,mock_validate) -> None:
        '''
        Test that the run_single_reliability_test method fails with no service_id
        Need to patch out __validate_reliability_test_id because it's called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
            )

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id')
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_dependency_id_required_not_provided(self,mock_post,mock_validate,mock_dependency) -> None:
        '''
        Test that the run_single_reliability_test method fails when dependency_id is required but not provided
        Need to patch out __validate_reliability_test_id and __reliability_test_id_requires_dependency_id because they're called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_dependency.return_value = True
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
            )

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id')
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_dependency_id_required_and_provided(self,mock_post,mock_validate,mock_dependency) -> None:
        '''
        Test that the run_single_reliability_test method works when dependency_id is required and provided
        Need to patch out __validate_reliability_test_id and __reliability_test_id_requires_dependency_id because they're called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_dependency.return_value = True
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
                dependency_id = mock_dependency_id,
            ),
            mock_data
        )

    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id')
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_dependency_id_not_required_and_not_provided(self,mock_post,mock_validate,mock_dependency) -> None:
        '''
        Test that the run_single_reliability_test method works when dependency_id is not required and not provided
        Need to patch out __validate_reliability_test_id and __reliability_test_id_requires_dependency_id because they're called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_dependency.return_value = False
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
            ),
            mock_data
        )
    
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id')
    @patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id')
    @patch('requests.post')
    def test_run_single_reliability_test_dependency_id_not_required_and_provided(self,mock_post,mock_validate,mock_dependency) -> None:
        '''
        Test that the run_single_reliability_test method fails when dependency_id is not required but provided
        Need to patch out __validate_reliability_test_id and __reliability_test_id_requires_dependency_id because they're called by run_single_reliability_test
        '''
        mock_validate.return_value = None
        mock_dependency.return_value = False
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_single_reliability_test(
                team_id = mock_team_id,
                reliability_test_id = mock_reliability_test_id,
                service_id = mock_service_id,
                dependency_id = mock_dependency_id,
            )

    #############################
    # run_all_reliability_tests()
    # - Test that the method works with config-based team_id
    # - Test that the method works with kwargs team_id
    # - Test that the method raises GremlinParameterError when team_id is not configured
    # - Test that the method raises GremlinParameterError if service_id is not provided.
    #############################

    @patch('requests.post')
    def test_run_all_reliability_tests_config_team_id(self,mock_post) -> None:
        '''
        Test that the run_all_reliability_tests method fails when team_id is not configured
        '''
        config.api_key = mock_api_key
        config.team_id = mock_team_id
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().run_all_reliability_tests(service_id = mock_service_id),
            mock_data
        )
        config.api_key = self.old_api_key
        config.team_id = self.old_team_id

    @patch('requests.post')
    def test_run_all_reliability_tests_kw_team_id(self, mock_post) -> None:
        '''
        Test that the run_all_reliability_tests method works when team_id is provided as a kwarg
        '''
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        self.assertEqual(
            GremlinAPIReliabilityTests().run_all_reliability_tests(team_id = mock_team_id, service_id = mock_service_id),
            mock_data
        )

    @patch('requests.post')
    def test_run_all_reliability_tests_no_team_id(self, mock_post) -> None:
        '''
        Test that the run_all_reliability_tests method fails when team_id is not provided
        '''
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_all_reliability_tests(service_id = mock_service_id)

    @patch('requests.post')
    def test_run_all_reliability_tests_no_service_id(self,mock_post) -> None:
        '''
        Test that the run_all_reliability_tests method fails when service_id is not configured
        '''
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = mock_json

        with self.assertRaises(GremlinParameterError):
            GremlinAPIReliabilityTests().run_all_reliability_tests(team_id = mock_team_id)