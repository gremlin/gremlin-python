# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging
import os
import time

from gremlinapi.alfi import GremlinALFI as alfi
from gremlinapi.attacks import GremlinAPIAttacks as Attacks
from gremlinapi.clients import GremlinAPIClients as Clients
from gremlinapi.companies import GremlinAPICompanies as Companies
from gremlinapi.config import GremlinAPIConfig
from gremlinapi.containers import GremlinAPIContainers as Containers
from gremlinapi.contracts import GremlinAPIContracts as Contracts
from gremlinapi.exceptions import *
from gremlinapi.executions import GremlinAPIExecutions as Executions
from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.halts import GremlinAPIHalts as Halts
from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.kubernetes import (GremlinAPIKubernetesAttacks as KubernetesAttacks,
                                   GremlinAPIKubernetesTargets as KubernetesTargets)
from gremlinapi.metadata import GremlinAPIMetadata as Metadata
from gremlinapi.orgs import GremlinAPIOrgs as Orgs
from gremlinapi.providers import GremlinAPIProviders as Providers
from gremlinapi.reports import GremlinAPIReports as Reports, GremlinAPIReportsSecurity as SecurityReports
from gremlinapi.scenarios import (GremlinAPIScenarios as Scenarios,
                                  GremlinAPIScenariosRecommended as RecommendedScenarios)
from gremlinapi.schedules import GremlinAPISchedules as Schedules
from gremlinapi.templates import GremlinAPITemplates as Templates
from gremlinapi.users import (GremlinAPIUsers as Users,
                              GremlinAPIUsersAuth as userAuth,
                              GremlinAPIUsersAuthMFA as userMFAuth)
from gremlinapi.util import get_version


__version__ = get_version()


# Logging Configuration
logging.getLogger('GremlinAPI.client').addHandler(logging.StreamHandler())

log = logging.getLogger('GremlinAPI.client')
log.setLevel(logging.DEBUG)

# API Settings
_api_host = 'https://api.gremlin.com'
_api_version = 'v1'

_api_key = os.getenv('GREMLIN_API_KEY', '')
_api_bearer_token = os.getenv('GREMLIN_BEARER_TOKEN', '')
_bearer_token_timestamp = None
_max_bearer_interval=os.getenv('GREMLIN_MAX_BEARER_INTERVAL', 86400)
_api_user = os.getenv('GREMLIN_USER', '')
_api_password = os.getenv('GREMLIN_PASSWORD', '')
_api_user_mfa_token = os.getenv('GREMLIN_USER_MFA_TOKEN', None)
_api_company = os.getenv('GREMLIN_COMPANY', '')
_api_team_guid = os.getenv('GREMLIN_TEAM_GUID', '')


GremlinAPIConfig.user = _api_user
GremlinAPIConfig.password = _api_password
GremlinAPIConfig.user_mfa_token_value = _api_user_mfa_token
GremlinAPIConfig.base_uri = f'{_api_host}/{_api_version}'
GremlinAPIConfig.company_name = _api_company
GremlinAPIConfig.api_key = _api_key
GremlinAPIConfig.bearer_token = _api_bearer_token
GremlinAPIConfig.bearer_timestamp = _bearer_token_timestamp
GremlinAPIConfig.max_bearer_interval = _max_bearer_interval


def login(user=GremlinAPIConfig.user, password=GremlinAPIConfig.password,
          company_name=GremlinAPIConfig.company_name, mfa_token_value=GremlinAPIConfig.user_mfa_token_value):
    if(not _bearer_token_timestamp
       or not _api_bearer_token
       or (time.monotonic() - GremlinAPIConfig.bearer_timestamp >= GremlinAPIConfig.max_bearer_interval)):
        if mfa_token_value:
            log.debug(f'MFA Login for {user} in company {company_name}')
            auth_response = userMFAuth.auth_user(user=user, password=password,
                                                 company=company_name, mfa_token_value=mfa_token_value)
        else:
            log.debug(f'Non-MFA Login for {user} in company {company_name}')
            auth_response = userAuth.auth_user(user=user, password=password, company=company_name)
        log.debug(auth_response)
        GremlinAPIConfig.bearer_token = auth_response
        GremlinAPIConfig.bearer_timestamp = time.monotonic()
    else:
        return GremlinAPIConfig.bearer_token
