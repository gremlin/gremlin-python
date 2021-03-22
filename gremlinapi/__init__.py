# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging
import os
import re
import time

from datetime import datetime, timezone

from gremlinapi.alfi import GremlinALFI as alfi
from gremlinapi.apikeys import GremlinAPIapikeys as apikeys
from gremlinapi.attack_helpers import (
    GremlinAttackHelper,
    GremlinAttackTargetHelper,
    GremlinTargetHosts,
    GremlinTargetContainers,
    GremlinAttackCommandHelper,
    GremlinResourceAttackHelper,
    GremlinStateAttackHelper,
    GremlinNetworkAttackHelper,
    GremlinCPUAttack,
    GremlinMemoryAttack,
    GremlinDiskSpaceAttack,
    GremlinDiskIOAttack,
    GremlinShutdownAttack,
    GremlinProcessKillerAttack,
    GremlinTimeTravelAttack,
    GremlinBlackholeAttack,
    GremlinDNSAttack,
    GremlinLatencyAttack,
    GremlinPacketLossAttack,
)
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
from gremlinapi.kubernetes import (
    GremlinAPIKubernetesAttacks as KubernetesAttacks,
    GremlinAPIKubernetesTargets as KubernetesTargets,
)
from gremlinapi.metadata import GremlinAPIMetadata as Metadata
from gremlinapi.metrics import GremlinAPIMetrics as Metrics
from gremlinapi.orgs import GremlinAPIOrgs as Orgs
from gremlinapi.providers import GremlinAPIProviders as Providers
from gremlinapi.reports import (
    GremlinAPIReports as Reports,
    GremlinAPIReportsSecurity as SecurityReports,
)
from gremlinapi.saml import GremlinAPISaml
from gremlinapi.scenario_helpers import (
    GremlinScenarioHelper,
    GremlinScenarioStep,
    GremlinILFIStep,
)
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioNode,
    GremlinScenarioAttackNode,
    GremlinScenarioILFINode,
    GremlinScenarioALFINode,
    GremlinScenarioDelayNode,
    GremlinScenarioStatusCheckNode,
)
from gremlinapi.scenarios import (
    GremlinAPIScenarios as Scenarios,
    GremlinAPIScenariosRecommended as RecommendedScenarios,
)
from gremlinapi.schedules import GremlinAPISchedules as Schedules
from gremlinapi.templates import GremlinAPITemplates as Templates
from gremlinapi.users import (
    GremlinAPIUsers as Users,
    GremlinAPIUsersAuth as userAuth,
    GremlinAPIUsersAuthMFA as userMFAuth,
)
from gremlinapi.util import get_version


__version__ = get_version()


# Logging Configuration
class SecretsFilter(logging.Filter):
    def filter(self, record):
        secret_length = 5
        if len(GremlinAPIConfig.api_key) >= secret_length:
            record.msg = re.sub(
                rf"{GremlinAPIConfig.api_key}[\'\s]?",
                "..." + GremlinAPIConfig.api_key[-4:],
                record.msg,
            )
        if len(GremlinAPIConfig.bearer_token) >= secret_length:
            record.msg = re.sub(
                rf"{GremlinAPIConfig.bearer_token}[\'\s]?",
                "..." + GremlinAPIConfig.bearer_token[-4:],
                record.msg,
            )
        if len(GremlinAPIConfig.password) >= secret_length:
            record.msg = re.sub(
                rf"{GremlinAPIConfig.password}[\'\s]?",
                "[PASSWORD REDACTED]",
                record.msg,
            )
        return record


logging_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

log = logging.getLogger("GremlinAPI.client")
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
log_handler.setFormatter(log_formatter)
log.addFilter(SecretsFilter())
log.addHandler(log_handler)
log.setLevel(
    logging_levels.get(
        os.getenv("GREMLIN_PYTHON_API_LOG_LEVEL", "WARNING"), logging.WARNING
    )
)

# API Settings
_api_host = "https://api.gremlin.com"
_api_version = "v1"

_api_key: str = os.getenv("GREMLIN_API_KEY", "")
_api_bearer_token: str = os.getenv("GREMLIN_BEARER_TOKEN", "")
_bearer_token_timestamp: str = ""
_max_bearer_interval: int = int(os.getenv("GREMLIN_MAX_BEARER_INTERVAL", 86400))
_api_user: str = os.getenv("GREMLIN_USER", "")
_api_password: str = os.getenv("GREMLIN_PASSWORD", "")
_api_user_mfa_token: str = os.getenv("GREMLIN_USER_MFA_TOKEN", "")
_api_company: str = os.getenv("GREMLIN_COMPANY", "")
_api_team_id: str = os.getenv("GREMLIN_TEAM_ID", "")

_http_proxy = os.getenv("GREMLIN_HTTP_PROXY", os.getenv("HTTP_PROXY", None))
_https_proxy = os.getenv("GREMLIN_HTTPS_PROXY", os.getenv("HTTPS_PROXY", None))


GremlinAPIConfig.user = _api_user  # type: ignore
GremlinAPIConfig.password = _api_password  # type: ignore
GremlinAPIConfig.user_mfa_token_value = _api_user_mfa_token  # type: ignore
GremlinAPIConfig.base_uri = f"{_api_host}/{_api_version}"  # type: ignore
GremlinAPIConfig.company_name = _api_company  # type: ignore
GremlinAPIConfig.api_key = _api_key  # type: ignore
GremlinAPIConfig.bearer_token = _api_bearer_token  # type: ignore
GremlinAPIConfig.bearer_timestamp = _bearer_token_timestamp  # type: ignore
GremlinAPIConfig.max_bearer_interval = _max_bearer_interval  # type: ignore
GremlinAPIConfig.http_proxy = _http_proxy  # type: ignore
GremlinAPIConfig.https_proxy = _https_proxy  # type: ignore


def _auth_response_to_bearer_config(auth_response):
    # if (log.getEffectiveLevel() == logging.DEBUG): log.debug(auth_response[0]['header'])
    GremlinAPIConfig.bearer_token = auth_response[0]["header"]
    GremlinAPIConfig.bearer_timestamp = datetime.now(timezone.utc)
    GremlinAPIConfig.bearer_expires = datetime.strptime(
        auth_response[0]["expires_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
    )


def login(
    email=GremlinAPIConfig.user,
    password=GremlinAPIConfig.password,
    company_name=GremlinAPIConfig.company_name,
    token=GremlinAPIConfig.user_mfa_token_value,
):
    if GremlinAPIConfig.user != email:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.debug(
                "Received user without value being present in config, updating config to match."
            )
        GremlinAPIConfig.user = email
    if GremlinAPIConfig.password != password:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.debug(
                "Received password without value being present in config, updating config to match."
            )
        GremlinAPIConfig.password = password
    if GremlinAPIConfig.company_name != company_name:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.debug(
                "Received company name without value being present in config, updating config to match."
            )
        GremlinAPIConfig.company_name = company_name
    if token and GremlinAPIConfig.user_mfa_token_value != token:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.debug(
                "Received mfa token without value being present in config, updating config to match."
            )
        GremlinAPIConfig.user_mfa_token_value = token
    if (
        not GremlinAPIConfig.bearer_timestamp
        or not GremlinAPIConfig.bearer_token
        or GremlinAPIConfig.is_bearer_expired()
    ):
        if token:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug(f"MFA Login for {email} in company {company_name}")
            auth_response = userMFAuth.auth_user(
                email=email, password=password, companyName=company_name, token=token
            )
        else:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug(f"Non-MFA Login for {email} in company {company_name}")
            auth_response = userAuth.auth_user(
                email=email, password=password, companyName=company_name
            )
        # if (log.getEffectiveLevel() == logging.DEBUG): log.debug(auth_response)
        _auth_response_to_bearer_config(auth_response)


def saml_login(email=GremlinAPIConfig.user, saml_assertion=None, relay_state=None):
    """
    Use SAML to perform an API login and return a bearer token

    :param email: email address of the user/service account
    :param saml_assertion:
    :param relay_state:
    :return:
    """
    if GremlinAPIConfig.user != email:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.debug(
                "Received user without value being present in config, updating config to match."
            )
        GremlinAPIConfig.user = email
    if not saml_assertion and relay_state:
        error_msg = f"Expecting a SAML assertion and relay state, received none"
        log.fatal(error_msg)
        raise GremlinParameterError(error_msg)
    acs_response = GremlinAPISaml.acs(
        SAMLResponse=saml_assertion, RelayState=relay_state
    )
    try:
        # redirect = re.search('window\.location="(.+?)"', acs_response).group(1)
        saml_session_code = re.search(
            "SamlSessionCode=(.+?)&", acs_response.headers["location"]
        ).group(1)
    except AttributeError:
        error_msg = "SAML Response did not provide a valid saml session code"
        log.fatal(error_msg)
        raise GremlinAuthError(error_msg)
    saml_sessions = GremlinAPISaml.sessions(code=saml_session_code)
    GremlinAPIConfig.bearer_token = saml_sessions["header"]
    return GremlinAPIConfig.bearer_token
