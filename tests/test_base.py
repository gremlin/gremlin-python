
import pytest
import responses
import re
from contextlib import nullcontext as does_not_raise

from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.exceptions import GremlinParameterError
from .util import (
     mock_team_id,
     mock_data,
)

class TestBase:
    '''
    Stripped down base class for testing API calls.
    Doesn't create any default tests, but does provide mocking and fixtures
    '''
    __test__ = False
    method = None
    kwargs = {}
    args = ()
    urls = {}

    @pytest.fixture
    def set_api_team_id(self):
        '''
        Ensure that team_id is set via config
        If it's not set, it's a property object, not a str.
        '''
        #print('Setting API Team ID')
        if isinstance(config.team_id,str):
            yield
        else:
            config.team_id = mock_team_id
            yield
            config.team_id = ""

    @pytest.fixture
    def unset_api_team_id(self):
        '''
        Ensure that team_id is not set via config
        '''
        #print('Unsetting API Team ID')
        if isinstance(config.team_id,str):
            old_api_team_id = config.team_id
            config.team_id = None
            yield
            config.team_id = old_api_team_id
        else:
            yield

    @pytest.fixture
    def unset_param_team_id(self):
        '''
        Ensure that team_id is not set via config
        '''
        #print('Unsetting PARAM Team ID')
        if self.kwargs.get('team_id') is None:
            yield
        else:
            old_param_team_id = self.kwargs.get('team_id')
            self.kwargs['team_id'] = None
            yield
            self.kwargs['team_id'] = old_param_team_id

    @pytest.fixture
    def mock_responses(self):
        '''
        Mock all responses to the wildcard url
        '''
        for method, urls in self.urls.items():
            for url in urls:
                if method == 'GET':
                    responses.get(
                        re.compile(url),
                        json = mock_data,
                        status=200
                    )
                elif method == 'POST':
                    responses.post(
                        re.compile(url),
                        json = mock_data,
                        status=200
                    )
        yield
        responses.reset()
    
class TestBasicMethod(TestBase):
    '''
    '''
    __test__ = False
    method = None
    kwargs = {}
    args = ()
    urls = {}

    @responses.activate
    @pytest.mark.usefixtures('mock_responses')
    def test_method(self):
        assert self.method(*self.args, **self.kwargs) == mock_data

class TestTeamIdBase:
    '''
    Base class for testing a method which requires a team_id
    '''

    __test__ = False
    method = None
    kwargs = {}
    args = ()
    urls = {}

    @pytest.fixture
    def set_api_team_id(self):
        '''
        Ensure that team_id is set via config
        If it's not set, it's a property object, not a str.
        '''
        #print('Setting API Team ID')
        if isinstance(config.team_id,str):
            yield
        else:
            config.team_id = mock_team_id
            yield
            config.team_id = ""

    @pytest.fixture
    def unset_api_team_id(self):
        '''
        Ensure that team_id is not set via config
        '''
        #print('Unsetting API Team ID')
        if isinstance(config.team_id,str):
            old_api_team_id = config.team_id
            config.team_id = None
            yield
            config.team_id = old_api_team_id
        else:
            yield

    @pytest.fixture
    def unset_param_team_id(self):
        '''
        Ensure that team_id is not set via config
        '''
        #print('Unsetting PARAM Team ID')
        if self.kwargs.get('team_id') is None:
            yield
        else:
            old_param_team_id = self.kwargs.get('team_id')
            self.kwargs['team_id'] = None
            yield
            self.kwargs['team_id'] = old_param_team_id

    @pytest.fixture
    def mock_responses(self):
        '''
        Mock all responses to the wildcard url
        '''
        for method, urls in self.urls.items():
            for url in urls:
                if method == 'GET':
                    responses.get(
                        re.compile(url),
                        json = mock_data,
                        status=200
                    )
                elif method == 'POST':
                    responses.post(
                        re.compile(url),
                        json = mock_data,
                        status=200
                    )
        yield
        responses.reset()
    
    @responses.activate
    @pytest.mark.usefixtures('unset_api_team_id','unset_param_team_id','mock_responses')
    def test_missing_team_id(self):
    #def test_missing_team_id(self,unset_api_team_id,unset_param_team_id,mock_responses):
        '''
        Ensure that ParamError comes from SDK instead of API error
            if team_id is not set via config or param
        '''
        with pytest.raises(GremlinParameterError, match='Endpoint requires a team_id or teamId, none supplied') as e:
            self.method(
                *self.args,
                **self.kwargs
            )
        assert 'team_id' in str(e.value)

    @responses.activate
    @pytest.mark.usefixtures('unset_api_team_id','mock_responses')
    def test_param_team_id(self):
    #def test_param_team_id(self,unset_api_team_id,mock_responses):
        '''
        Test that team_id can be passed as a parameter.
        This checks a regression where **kwargs is not properly
            passed to __required_team_endpoint
        '''
        assert self.method(team_id = mock_team_id,*self.args,**self.kwargs) == mock_data

    @responses.activate
    @pytest.mark.usefixtures('unset_param_team_id','set_api_team_id','mock_responses')
    def test_config_team_id(self):
    #def test_config_team_id(self,unset_param_team_id,set_api_team_id,mock_responses):
        '''
        Test that team_id can be set via config
        '''
        assert self.method(*self.args,**self.kwargs) == mock_data

class TestRequiredParamBase:
    '''
    Base class for testing a method which requires a parameter
    '''
    __test__ = False
    method = None
    kwargs = {}
    args = ()
    urls = {}
    param_name = None

    @pytest.fixture
    def mock_responses(self):
        '''
        Mock all responses to the wildcard url
        '''
        for method, urls in self.urls.items():
            for url in urls:
                if method == 'GET':
                    responses.add(responses.Response(
                        responses.GET,
                        re.compile(url),
                        json = mock_data,
                        status=200
                    ))
                elif method == 'POST':
                    responses.add(responses.Response(
                        responses.POST,
                        re.compile(url),
                        json = mock_data,
                        status=200
                    ))
        yield
        responses.reset()

    @pytest.fixture
    def unset_param(self):
        '''
        Ensure that param is not set via param
        '''
        old_param = self.kwargs.get(self.param_name)
        self.kwargs[self.param_name] = None
        yield
        self.kwargs[self.param_name] = old_param

    @responses.activate
    def test_method_with_param(self,mock_responses):
        '''
        Ensure that method works when param is set
        '''
        assert self.method(*self.args,**self.kwargs) == mock_data

    @responses.activate
    def test_missing_param(self,mock_responses,unset_param):
        '''
        Ensure that ParamError comes from SDK instead of API error
            if param is not set via param
        '''
        with pytest.raises(GremlinParameterError, match=f'{self.param_name}' + r'*'):
            self.method(
                *self.args,
                **self.kwargs
            )

class TestOptionalParamBase:
    '''
    Base class for testing a method which requires a parameter
    '''
    __test__ = False
    method = None
    kwargs = {}
    args = ()
    urls = {}
    param_name = None

    @pytest.fixture
    def mock_responses(self):
        '''
        Mock all responses to the wildcard url
        '''
        for method, urls in self.urls.items():
            for url in urls:
                if method == 'GET':
                    responses.add(responses.Response(
                        responses.GET,
                        re.compile(url),
                        json = mock_data,
                        status=200
                    ))
                elif method == 'POST':
                    responses.add(responses.Response(
                        responses.POST,
                        re.compile(url),
                        json = mock_data,
                        status=200
                    ))
        yield
        responses.reset()

    @pytest.fixture
    def unset_param(self):
        '''
        Ensure that param is not set via param
        '''
        old_param = self.kwargs.get(self.param_name)
        self.kwargs[self.param_name] = None
        yield
        self.kwargs[self.param_name] = old_param

    @responses.activate
    def test_method_with_param(self,mock_responses):
        '''
        Ensure that method works when param is set
        '''
        assert self.method(*self.args,**self.kwargs) == mock_data

    @responses.activate
    def test_missing_param(self,mock_responses,unset_param):
        '''
        Ensure that ParamError comes from SDK instead of API error
            if param is not set via param
        '''
        assert self.method(*self.args,**self.kwargs) == mock_data