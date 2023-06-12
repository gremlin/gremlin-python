
import pytest
import responses

from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.reliability_tests import GremlinAPIReliabilityTests
from .test_base import (
    TestTeamIdBase,
    TestRequiredParamBase,
    TestBase
)
from gremlinapi.exceptions import GremlinParameterError
import requests
import os
import re
from .util import (
     api_key as mock_api_key,
     mock_data,
     mock_service_id,
     mock_reliability_test_id,
     mock_dependency_id,
     mock_base_url
)

config.api_key = mock_api_key

class TestListReliabilityTestTypes():

    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        '''
        method = GremlinAPIReliabilityTests.list_reliability_test_types
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests*'
            ]
        }

class TestListServiceReliabilityTests():
    
    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        '''
        method = GremlinAPIReliabilityTests.list_service_reliability_test_runs
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests.*'
            ]
        }
        kwargs = {
            'service_id': mock_service_id
        }
    
    class TestServiceId(TestRequiredParamBase):
        '''
        Test service_id dependency
        '''
        method = GremlinAPIReliabilityTests.list_service_reliability_test_runs
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests/runs.*'
            ]
        }
        kwargs = {
            'service_id': mock_service_id
        }
        param_name = 'service_id'

class TestListServiceReliabilityTestRunsByType():
     
    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        '''
        method = GremlinAPIReliabilityTests.list_service_reliability_test_runs_by_type
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + '/reliability-tests/' + mock_reliability_test_id + r'/runs*'
            ]
        }
        kwargs = {
            'service_id': mock_service_id,
            'reliability_test_id': mock_reliability_test_id
        }

    class TestServiceId(TestRequiredParamBase):
        '''
        Test service_id dependency
        '''
        method = GremlinAPIReliabilityTests.list_service_reliability_test_runs_by_type
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + '/reliability-tests/' + mock_reliability_test_id + r'/runs*'
            ]
        }
        kwargs = {
            'service_id': mock_service_id,
            'reliability_test_id': mock_reliability_test_id
        }
        param_name = 'service_id'

    class TestReliabilityTestId(TestRequiredParamBase):
        '''
        Test reliability_test_id dependency
        '''
        method = GremlinAPIReliabilityTests.list_service_reliability_test_runs_by_type
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + '/reliability-tests/' + mock_reliability_test_id + r'/runs*'
            ]
        }
        args = ()
        kwargs = {
            'service_id': mock_service_id,
            'reliability_test_id': mock_reliability_test_id
        }
 
        param_name = 'reliability_test_id'

class TestListReliabilityTestNotifications():

    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        '''
        method = GremlinAPIReliabilityTests.list_reliability_test_notifications
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests/notifications*'
            ]
        }

class TestRunSingleReliabilityTest():
    '''
    This method has some private methods used to validate the inputs
    As a result, the mocks are more complicated because we have to manipulate those
        private methods to return the correct values for each test case.
    '''

    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        We can use the super() methods, but we need to add some extra fixtures for those
            private methods.
        '''
        method = GremlinAPIReliabilityTests.run_single_reliability_test
        __test__ = False
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests*'
            ],
            'POST': [
                mock_base_url + '/reliability-tests/' + mock_reliability_test_id + '/runs'
            ]
        }
        kwargs = {
            'service_id': mock_service_id,
            'reliability_test_id': mock_reliability_test_id,
            'dependency_id': mock_dependency_id
        }

        @pytest.fixture
        def bypass_validate_reliability_test_id(self, mocker):
            '''
            Mock the call to __validate_reliability_test_id
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id', return_value=None)

        @pytest.fixture
        def dependency_required_true(self, mocker):
            '''
            Override __reliability_test_id_requires_dependency_id to return True
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id', return_value=True)

        @pytest.fixture
        def dependency_required_false(self, mocker):
            '''
            Override __reliability_test_id_requires_dependency_id to return False
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id', return_value=False)

        @pytest.fixture
        def unset_dependency_id(self, mocker):
            '''
            Unset the dependency_id
            '''
            if 'dependency_id' in self.kwargs:
                old_dependency_id = self.kwargs['dependency_id']
                self.kwargs.pop('dependency_id')
                yield
                self.kwargs['dependency_id'] = old_dependency_id
            else:
                yield

        @pytest.mark.usefixtures('unset_api_team_id','unset_param_team_id','mock_responses','bypass_validate_reliability_test_id','dependency_required_true')
        def test_missing_team_id(self, mocker):
            '''
            Must mock the call to __validate_reliability_test_id,
                otherwise ITS team_id check will be used.
            '''
            super().test_missing_team_id()


        @pytest.mark.usefixtures('unset_api_team_id','mock_responses','bypass_validate_reliability_test_id','dependency_required_true')
        def test_param_team_id(self, mocker):
            '''
            '''
            super().test_param_team_id()


        @pytest.mark.usefixtures('unset_param_team_id','set_api_team_id','mock_responses','bypass_validate_reliability_test_id','dependency_required_true')
        def test_config_team_id(self, mocker):
            '''
            '''
            super().test_config_team_id()


    class TestDependencyId(TestBase):
        '''
        Test dependency_id dependency
        Using the TestBase class because none of the canned methods will work at all.
        '''
        method = GremlinAPIReliabilityTests.run_single_reliability_test
        __test__ = True
        urls = {
            'GET': [
                mock_base_url + r'/reliability-tests*'
            ],
            'POST': [
                mock_base_url + '/reliability-tests/' + mock_reliability_test_id + '/runs'
            ]
        }
        kwargs = {
            'service_id': mock_service_id,
            'reliability_test_id': mock_reliability_test_id,
            'dependency_id': mock_dependency_id
        }

        @pytest.fixture
        def bypass_validate_reliability_test_id(self, mocker):
            '''
            Mock the call to __validate_reliability_test_id
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__validate_reliability_test_id', return_value=None)

        @pytest.fixture
        def dependency_required_true(self, mocker):
            '''
            Override __reliability_test_id_requires_dependency_id to return True
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id', return_value=True)

        @pytest.fixture
        def dependency_required_false(self, mocker):
            '''
            Override __reliability_test_id_requires_dependency_id to return False
            '''
            mocker.patch.object(GremlinAPIReliabilityTests, '_GremlinAPIReliabilityTests__reliability_test_id_requires_dependency_id', return_value=False)

        @pytest.fixture
        def unset_dependency_id(self, mocker):
            '''
            Unset the dependency_id
            '''
            if 'dependency_id' in self.kwargs:
                old_dependency_id = self.kwargs['dependency_id']
                self.kwargs.pop('dependency_id')
                yield
                self.kwargs['dependency_id'] = old_dependency_id
            else:
                yield

        @pytest.mark.usefixtures('dependency_required_true','mock_responses','bypass_validate_reliability_test_id','unset_dependency_id')
        def test_dependency_id_required_and_not_provided(self, mocker):
            '''
            If dependency is required and is not provided, an exception should be raised specifically for the dependency_id
            '''
            with pytest.raises(GremlinParameterError) as e:
                self.method(**self.kwargs)
            assert 'dependency_id' in str(e.value)

        @pytest.mark.usefixtures('dependency_required_true','mock_responses','bypass_validate_reliability_test_id','set_api_team_id')
        @responses.activate
        def test_dependency_id_required_and_provided(self, mocker):
            '''
            If dependency id is required and is provided, the request should return properly
            '''
            assert self.method(**self.kwargs) == mock_data

        @pytest.mark.usefixtures('dependency_required_false','mock_responses','bypass_validate_reliability_test_id')
        def test_dependency_id_not_required_and_provided(self, mocker):
            '''
            If dependency id is not required and is provided, an exception should be raised specifically for the dependency_id
            '''
            with pytest.raises(GremlinParameterError) as e:
                self.method(**self.kwargs)
            assert 'dependency_id' in str(e.value)

        @pytest.mark.usefixtures('dependency_required_false','mock_responses','bypass_validate_reliability_test_id','unset_dependency_id','set_api_team_id')
        @responses.activate
        def test_dependency_id_not_required_and_not_provided(self, mocker):
            '''
            If dependency id is not required and is not provided, the request should return properly
            '''
            assert self.method(**self.kwargs) == mock_data

class TestRunAllReliabilityTests():
    class TestTeamId(TestTeamIdBase):
        '''
        Standard team_id tests
        '''
        method = GremlinAPIReliabilityTests.run_all_reliability_tests
        __test__ = True
        urls = {
            'POST': [
                mock_base_url + '/services/' + mock_service_id + r'/baseline*'
            ]
        }
        kwargs = {
            'service_id': mock_service_id
        }