# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError,
    HTTPBadHeader
)

from gremlinapi.config import GremlinAPIConfig
from gremlinapi.util import get_version

try:
    import requests
    import requests.adapters
except ImportError:
    requests = None
    import urllib3

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIHttpClient(object):
    @classmethod
    def api_call(cls, method, uri, *args, **kwargs):
        error_message = f'This function is not implemented, please consume the proper http library for your environment'
        log.fatal(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    def base_uri(cls, uri):
        if not uri.startswith('http') and GremlinAPIConfig.base_uri not in uri:
            uri = f'{GremlinAPIConfig.base_uri}{uri}'
        return uri

    @classmethod
    def header(cls, *args, **kwargs):
        api_key = kwargs.get('api_key', None)
        bearer_token = kwargs.get('bearer_token', None)
        header = dict()
        if not (api_key and bearer_token):
            if GremlinAPIConfig.bearer_token:
                bearer_token = GremlinAPIConfig.bearer_token
            if GremlinAPIConfig.api_key:
                api_key = GremlinAPIConfig.api_key
        if api_key and not bearer_token:
            if "Key" in api_key:
                header['Authorization'] = api_key
            else:
                header['Authorization'] = f'Key {api_key}'
        elif bearer_token:
            if "Bearer" in bearer_token:
                header['Authorization'] = bearer_token
            else:
                header['Authorization'] = f'Bearer {bearer_token}'
        else:
            error_msg = f'Missing API Key or Bearer Token, none supplied: {api_key}, {bearer_token}'
            log.fatal(error_msg)
            # raise HTTPBadHeader(error_msg)
        header['X-Gremlin-Agent'] = f'gremlin-sdk-python/{get_version()}'
        return header

    @classmethod
    def proxies(cls):
        error_message = f'This function is not implemented, please consume the proper http library for your environment'
        log.fatal(error_message)
        raise NotImplementedError(error_message)


class GremlineAPIRequestsClient(GremlinAPIHttpClient):
    @classmethod
    def proxies(cls):
        proxies = dict()

        if GremlinAPIConfig.http_proxy and type(GremlinAPIConfig.http_proxy) is str:
            proxies['http'] = GremlinAPIConfig.http_proxy
        if GremlinAPIConfig.https_proxy and type(GremlinAPIConfig.https_proxy) is str:
            proxies['https'] = GremlinAPIConfig.https_proxy

        return proxies

    @classmethod
    def api_call(cls, method, endpoint, *args, **kwargs):

        request_methods = {
            "HEAD": requests.head,
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch,
        }

        # uri = f'{GremlinAPIConfig.base_uri}{endpoint}'
        uri = cls.base_uri(endpoint)
        client = request_methods.get(method.upper())
        raw_content = kwargs.pop("raw_content", False)
        data = None
        if 'data' in kwargs:
            data = kwargs.pop('data')
        elif 'body' in kwargs:
            if "Content-Type" not in kwargs["headers"]:
                kwargs["headers"]["Content-Type"] = "application/json"
            data = kwargs.pop('body')
            if not isinstance(data, str):
                data = json.dumps(data)
            log.debug(f'body: {data}')

        kwargs['proxies'] = cls.proxies()
        log.debug(f'httpd client kwargs: {kwargs}')

        if data:
            resp = client(uri, data=data, **kwargs)
        else:
            resp = client(uri, **kwargs)

        if resp.status_code >= 400:
            error_msg = f'error {resp.status_code} : {resp.reason}'
            log.warning(error_msg)
            log.debug(f'{client}\n{uri}\n{data}\n{kwargs}')
            raise HTTPError(error_msg)

        if raw_content:
            body = resp.content
        else:
            try:
                body = resp.json()
            except ValueError:
                # No JSON in response
                try:
                    body = str(resp.content, resp.encoding)
                except TypeError:
                    # Response must be empty, return something nice
                    body = 'Success'

        return resp, body


class GremlinAPIurllibClient(GremlinAPIHttpClient):
    """Fallback library in the event requests library is unavailable."""
    @classmethod
    def api_call(cls, method, endpoint, *args, **kwargs):

        log.warning(f'The request to {endpoint} is using the urllib3 library. Consider installing th requests library.')
        form_data = None
        request_body = None

        if 'data' in kwargs:
            form_data = kwargs.pop('data')
        elif 'body' in kwargs:
            if "Content-Type" not in kwargs["headers"]:
                kwargs["headers"]["Content-Type"] = "application/json"
            request_body = json.dumps(kwargs.pop("body"))

        uri = f'{GremlinAPIConfig.base_uri}{endpoint}'

        if GremlinAPIConfig.https_proxy and type(GremlinAPIConfig.https_proxy) is str:
            http_client = urllib3.ProxyManager(GremlinAPIConfig.https_proxy)
        elif GremlinAPIConfig.http_proxy and type(GremlinAPIConfig.http_proxy) is str:
            http_client = urllib3.ProxyManager(GremlinAPIConfig.http_proxy)
        else:
            http_client = urllib3.PoolManager()

        if form_data:
            resp = http_client.request(method, uri, fields=form_data, **kwargs)
        elif request_body:
            resp = http_client.request(method, uri, body=request_body, **kwargs)
        else:
            resp = http_client.request(method, uri, **kwargs)
        log.debug(resp)

        if resp.status >= 400:
            log.debug(f'Failed response: {resp.status}\n{http_client}\n{uri}\n{kwargs}\n{resp}')
            raise HTTPError(resp)

        body = json.loads(resp.data)
        return resp, body


def get_gremlin_httpclient():
    if requests:
        return GremlineAPIRequestsClient
    else:
        return GremlinAPIurllibClient

