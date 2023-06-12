import logging
import json

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from typing import Union, Type

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import (
    get_gremlin_httpclient,
    GremlinAPIHttpClient
)

log = logging.getLogger("GremlinAPI.client")


class GremlinAPIReliabilityTests(GremlinAPI):


    @classmethod
    def __validate_reliability_test_id(
        cls,
        reliability_test_id: str,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient()
    ) -> None:
        '''
        Ensure that a reliablity test ID is valid
        '''
        all_tests = [ x['guid'] for x in cls.list_reliability_test_types()['global'] ]
        if reliability_test_id not in all_tests:
            raise GremlinParameterError(f'Reliability test ID {reliability_test_id} is not valid.')
        
    @classmethod
    def validate_reliability_test_id(cls,
        reliability_test_id: str
    ):
        '''
        '''
        cls.__validate_reliability_test_id(reliability_test_id)

    @classmethod
    def __reliability_test_id_requires_dependency_id(
        cls,
        reliability_test_id: str
    ) -> bool:
        if reliability_test_id in ('blackhole-test','latency-test','certificate-expiry'):
            return True


    @classmethod
    def list_reliability_test_types(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        """
        List all types of reliability tests.
        These types represent the different types of tests/experiments
            that can be run against a service in Gremlin.
        """
        method = "GET"
        endpoint = cls._required_team_endpoint("/reliability-tests", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
    

    @classmethod
    def list_service_reliability_test_runs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        '''
        List all reliability tests that have been run for a particular service ID
        '''
        method = "GET"
        service_id = cls._error_if_not_param("service_id", **kwargs)
        endpoint = cls._required_team_endpoint(
            f'/reliability-tests/runs/?serviceId={service_id}', **kwargs
        )
        payload = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


    @classmethod
    def list_service_reliability_test_runs_by_type(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        '''
        List all reliability tests of a specific type that have been run for a particular service ID
        '''
        method = "GET"
        service_id = cls._error_if_not_param("service_id", **kwargs)
        reliability_test_id = cls._error_if_not_param("reliability_test_id", **kwargs)
        # TODO: Removing page_size for now, since it's not fully working.
        #page_size = cls._info_if_not_param("pageSize", **kwargs)
        #if not page_size:
        #    endpoint = cls._required_team_endpoint(
        #        f'/reliability-tests/{reliability_test_id}/runs/?serviceId={service_id}', **kwargs)
        #else:
        #    endpoint = cls._required_team_endpoint(
        #        f'/reliability-tests/{reliability_test_id}/runs/?serviceId={service_id}&pageSize={page_size}', **kwargs)
        endpoint = cls._required_team_endpoint(
            f'/reliability-tests/{reliability_test_id}/runs/?serviceId={service_id}', **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


    @classmethod
    def list_reliability_test_notifications(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        '''
        List all reliability test notifications for this team
        '''
        method = "GET"
        endpoint = cls._required_team_endpoint("/reliability-tests/notifications", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
    

    @classmethod
    def run_single_reliability_test(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        '''
        Run a single reliability test against a service
        '''
        method = "POST"

        reliability_test_id = cls._error_if_not_param("reliability_test_id", **kwargs)
        cls.__validate_reliability_test_id(reliability_test_id)

        service_id = cls._error_if_not_param("service_id", **kwargs)
        data = {
            'serviceId': service_id
        }

        if cls.__reliability_test_id_requires_dependency_id(reliability_test_id):
            dependency_id = cls._error_if_not_param("dependency_id", **kwargs)
            data['dependencyId'] = dependency_id
        else:
            if 'dependency_id' in kwargs or 'dependencyId' in kwargs:
                raise GremlinParameterError(
                    'The reliability test you are trying to run does not require a dependency_id'
                )

        endpoint = cls._required_team_endpoint(f"/reliability-tests/{reliability_test_id}/runs", **kwargs)
        payload = cls._payload(**{"headers": https_client.header(), "data": json.dumps(data)})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    
    @classmethod
    def run_all_reliability_tests(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        '''
        Run all reliability tests for a service
        '''
        method = "POST"
        service_id = cls._error_if_not_param("service_id", **kwargs)
        endpoint = cls._required_team_endpoint(f"/services/{service_id}/baseline", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        data = {
            'startBaselineRequest': ''
        }
        payload = cls._payload(**{"headers": https_client.header(), "data": json.dumps(data)})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def get_service_reliability_score(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> int:
        '''
        Retrieve current score for a service
        '''
        method = "GET"
        service_id = cls._error_if_not_param("service_id", **kwargs)
        endpoint = cls._required_team_endpoint(f"/reliability-management/services/{service_id}", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body['score']