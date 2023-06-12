import pytest
import responses

from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.orgs import GremlinAPIOrgs
from .test_base import (
    TestTeamIdBase,
    TestRequiredParamBase,
    TestBase,
    TestBasicMethod,
    TestOptionalParamBase
)
from gremlinapi.exceptions import GremlinParameterError
import requests
import os
import re
from .util import (
     api_key as mock_api_key,
     mock_base_url,
     mock_org_id,
)

config.api_key = mock_api_key

class TestListOrgs():

    class BasicMethod(TestBasicMethod):
        __test__ = True
        method = GremlinAPIOrgs.list_orgs
        urls = {
            'GET': f'{mock_base_url}/orgs',
        }

class TestGetOrg():

    class BasicMethod(TestBasicMethod):
        __test__ = True
        method = GremlinAPIOrgs.get_org
        urls = {
            'GET': [
                mock_base_url + r'/orgs*'
            ]
        }
        kwargs = {
            'identifier': mock_org_id
        }

    class RequiredParamIdentifier(TestRequiredParamBase):
        __test__ = True
        method = GremlinAPIOrgs.get_org
        urls = {
            'GET': [
                mock_base_url + r'/orgs*'
            ]
        }
        kwargs = {
            'identifier': mock_org_id
        }
        param_name = 'identifier'

    class OptionalParamAddUser(TestOptionalParamBase):
        __test__ = True
        method = GremlinAPIOrgs.get_org
        urls = {
            'GET': [
                mock_base_url + r'/orgs*'
            ]
        }
        kwargs = {
            'identifier': mock_org_id,
            'add_user': True
        }
        param_name = 'add_user'

class TestCreateOrg():

    class BasicMethod(TestBasicMethod):
        __test__ = True
        method = GremlinAPIOrgs.create_org
        urls = {
            'POST': [
                f'{mock_base_url}/orgs'
            ]
        }
        kwargs = {
            'name': 'test_org',
        }

class TestNewCertificate():
    pass