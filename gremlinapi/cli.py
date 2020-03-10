# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import functools
import logging


logging.getLogger('GremlinAPI.client')


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



