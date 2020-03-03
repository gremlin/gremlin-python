# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging
import os
import time

from gremlinapi.alfi import GremlinALFI
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.clients import GremlinAPIClients
from gremlinapi.companies import GremlinAPICompanies
from gremlinapi.containers import GremlinAPIContainers
from gremlinapi.contracts import GremlinAPIContracts
from gremlinapi.exceptions import *
from gremlinapi.executions import GremlinAPIExecutions
from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.halts import GremlinAPIHalts
from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks, GremlinAPIKubernetesTargets
from gremlinapi.metadata import GremlinAPIMetadata
from gremlinapi.orgs import GremlinAPIOrgs
from gremlinapi.providers import GremlinAPIProviders
from gremlinapi.reports import GremlinAPIReports, GremlinAPIReportsSecurity
from gremlinapi.scenarios import GremlinAPIScenarios, GremlinAPIScenariosRecommended
from gremlinapi.schedules import GremlinAPISchedules
from gremlinapi.templates import GremlinAPITemplates
from gremlinapi.users import GremlinAPIUsers, GremlinAPIUsersAuth, GremlinAPIUsersAuthMFA
from gremlinapi.util import get_version


__version__ = get_version()


# Logging Configuration
logging.getLogger('GremlinAPI.client').addHandler(logging.StreamHandler())


# API Settings
_api_host = 'https://api.gremlin.com'
_api_version = 'v1'

_api_key = os.getenv('GREMLIN_API_KEY', '')
_api_bearer_token = os.getenv('GREMLIN_BEARER_TOKEN', '')
_api_username = os.getenv('GREMLIN_USER', '')
_api_password = os.getenv('GREMLIN_PASSWORD', '')
_api_user_mfa_token = os.getenv('GREMLIN_USER_MFA_TOKEN', None)
_api_company = os.getenv('GREMLIN_COMPANY', '')
_api_team_guid = os.getenv('GREMLIN_TEAM_GUID', '')

_max_bearer_interval=os.getenv('GREMLIN_MAX_BEARER_INTERVAL', 86400)
_bearer_token_timestamp = None

def login(api_username=_api_username, api_password=_api_password,
          api_company=_api_company, mfa_token_value=_api_user_mfa_token):
    if(not _bearer_token_timestamp
       or not _api_bearer_token
       or (time.monotonic() - _bearer_token_timestamp >= cls.max_bearer_interval)):
        if mfa_token_value:
            auth_response = GremlinAPIUsersAuthMFA.auth_user(user=api_username, password=api_password,
                                                             company=api_company, mfa_token_value=mfa_token_value)
        else:
            auth_response = GremlinAPIUsersAuth.auth_user(user=api_username, password=api_password, company=api_company)
        _api_bearer_token = auth_response
        _bearer_token_timestamp = time.monotonic()
    else:
        return _api_bearer_token
