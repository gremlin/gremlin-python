# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import argparse
import functools
import importlib
import logging
import os
import sys

from gremlinapi.config import GremlinAPIConfig
from gremlinapi.exceptions import GremlinAuthError

log = logging.getLogger('GremlinAPI.client')


cli_actions = dict()

def register_cli_action(cls_names, required=tuple(), optional=tuple()):
    def wrap(f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)

        in_obj = True
        classes = cls_names
        if type(classes) != tuple:
            classes = (classes,)

        for cls_name in classes:
            if cls_name not in cli_actions:
                cli_actions[cls_name] = {}
            action = f.__name__.replace("_","-")
            cli_actions[cls_name][action] = (required, optional, in_obj)

        return wrapped_f
    return wrap

def _base_args():
    p = argparse.ArgumentParser(description="Gremlin API Command Line Interface")
    p.add_argument("--version",
                   help="Display the version.",
                   type=bool,
                   action="store",
                   dest="version",
                   default=False)
    p.add_argument("-v", "--verbose",
                   help="Verbose Mode",
                   type=bool,
                   action="store",
                   dest="verbose",
                   default=False)
    p.add_argument("-d", "--debug",
                   help="Debug mode (may expose authentication credentials to logs!)",
                   type=bool,
                   action="store",
                   dest="debug",
                   default=False)
    auth = p.add_argument_group('Authentication Configuration Options')
    auth.add_argument("-a", "--apikey",
                      help="User provided API key",
                      type=str,
                      action="store",
                      dest="gremlin_api_key",
                      default=os.getenv('GREMLIN_API_KEY', None))
    auth.add_argument("-b", "--bearer",
                      help="User provided bearer token",
                      type=str,
                      action="store",
                      dest="gremlin_bearer",
                      default=os.getenv('GREMLIN_BEARER_TOKEN', None))
    auth.add_argument("-i", "--bearer-interval",
                      help="Maximum bearer token age in seconds if using login methods",
                      type=int,
                      action="store",
                      dest="max_bearer_interval",
                      default=os.getenv('GREMLIN_MAX_BEARER_INTERVAL', 86400))
    auth.add_argument("-u", "--user",
                      help="Gremlin user (email) to use for login functions",
                      type=str,
                      dest="gremlin_user",
                      default=os.getenv('GREMLIN_USER', ''))
    auth.add_argument("-p", "--password",
                      help="Password to use for login functions (will be exposed in logs if debug mode is enabled!)",
                      type=str,
                      action="store",
                      dest="gremlin_password",
                      default=os.getenv('GREMLIN_PASSWORD', ''))
    auth.add_argument("-m", "--mfa",
                      help="MFA OTP Token for login functions",
                      type=int,
                      action="store",
                      dest="gremlin_user_mfa_token",
                      default=os.getenv('GREMLIN_USER_MFA_TOKEN', None))
    auth.add_argument("-c", "--company",
                      help="Company Name, as it appears in the Gremlin UI or API, for user login functions",
                      type=str,
                      action="store",
                      dest="gremlin_company",
                      default=os.getenv('GREMLIN_COMPANY', ''))
    auth.add_argument("-t", "--team_id",
                      help="Gremlin Team ID, required for RBAC enabled accounts",
                      type=str,
                      action="store",
                      dest="gremlin_team_id",
                      default=os.getenv('GREMLIN_TEAM_ID', ''))
    return p

def _get_parser(cli_module):
    parser = _base_args()
    return cli_module.extend_parser(parser)

def _parse_args():
    parser = _base_args()
    #args = parser.parse_known_args(sys.argv[1:])
    (options, args) = parser.parse_known_args(sys.argv)
    cli_module = importlib.import_module('gremlinapi.cli.cli')
    parser = _get_parser(cli_module)
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except Exception:
        pass
    # Sanity check input
    try:
        if not (args.gremlin_user and args.gremlin_password) and not (args.gremlin_bearer or args.gremlin_api_key):
            error_msg = f'No form of API authentication provided: {args}'
            log.fatal(error_msg)
            raise GremlinAuthError(error_msg)
        elif args.gremlin_api_key:
            log.debug(f'API authentication supplied: key {args.gremlin_api_key}')
        elif args.bearer:
            log.debug(f'Bearer supplied at CLI runtime: {args.bearer}')
            GremlinAPIConfig.bearer_token = args.bearer
        elif args.gremlin_user and args.gremlin_password:
            log.debug(f'User authentication provided for user: {args.gremlin_user}')
            GremlinAPIConfig.user = args.gremlin_user
            GremlinAPIConfig.password = args.gremlin_password
            if args.gremlin_user_mfa_token:
                log.debug(f'MFA token provided for user {args.gremlin_user}')
                GremlinAPIConfig.user_mfa_token_value = args.gremlin_user_mfa_token
        else:
            error_msg = f'Unexpected state, authentication logic fallthrough: {args}'
            log.fatal(error_msg)
            raise GremlinAuthError(error_msg)
    except GremlinAuthError:
        parser.print_help()


def main():
    _parse_args()






