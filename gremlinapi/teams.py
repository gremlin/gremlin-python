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

class GremlinAPITeam(GremlinAPI):

    @classmethod
    def get_teams(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
    ) -> dict:
        """
        Get all teams
        """
        method = 'GET'
        endpoint = '/teams'
        payload = cls._payload(**{"headers": https_client.header()})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def delete_team(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        """
        Delete a team
        """
        method = 'DELETE'
        team_id = cls._error_if_not_param("team_id", **kwargs)
        endpoint = f'/teams/{team_id}'
        payload = cls._payload(**{"headers": https_client.header()})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def update_team(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        """
        Update a team
        """
        method = 'PATCH'
        team_id = cls._error_if_not_param("team_id", **kwargs)
        endpoint = f'/teams/{team_id}'
        data = kwargs
        data.pop('team_id')
        payload = cls._payload(**{"headers": https_client.header(),"data": json.dumps(data)})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def get_config_yaml(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        """
        Get the config.yaml for a team
        """
        method = 'GET'
        endpoint = cls._required_team_endpoint("/teams/client/install", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def get_team(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        """
        Get a team
        """
        method = 'GET'
        team_id = cls._error_if_not_param("team_id", **kwargs)
        endpoint = f'/teams/{team_id}'
        payload = cls._payload(**{"headers": https_client.header()})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body
    
    @classmethod
    def get_kubectl_install_manifest(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        """
        Get the kubectl install manifest for a team
        """
        method = 'GET'
        endpoint = cls._required_team_endpoint("/teams/kubernetes/install", **kwargs)
        payload = cls._payload(**{"headers": https_client.header()})
        (resp,body) = https_client.api_call(method, endpoint, **payload)
        return body