# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging
import functools, warnings, inspect

log = logging.getLogger("GremlinAPI.client")

_version = "0.15.4"


def get_version():
    return _version


string_types = (type(b""), type(""), type(f""))

GREMLIN_OAUTH_LOGIN = "https://api.gremlin.com/v1/oauth/login"
GREMLIN_OAUTH_COMPANIES_URI = "https://api.gremlin.com/v1/companies"
GREMLIN_SSO_USER_AUTH = "https://api.gremlin.com/v1/users/auth/sso"
GREMLIN_OAUTH_CALLBACK = "https://api.gremlin.com/v1/oauth/callback"


def experimental(func):
    """
    This is a decorator that will be used on in-progress or
    otherwise incomplete functions and objects.
    """
    if inspect.isclass(func) or inspect.isfunction(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            message = "Call to experimental function `{}` ** Please proceed with caution **".format(
                func.__name__
            )
            warnings.warn(message)
            return func(*args, **kwargs)

        return new_func

    elif isinstance(func, string_types):

        def decorator(func1):
            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                message = "Call to experimental function `{}` ** %s **" % func
                warnings.warn(message)
                return func1(*args, **kwargs)

            return new_func1

        return decorator


def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    if inspect.isclass(reason) or inspect.isfunction(reason):

        @functools.wraps(reason)
        def new_func(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)  # turn off filter
            warnings.warn(
                "Call to deprecated function {}.".format(reason.__name__),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)  # reset filter
            return reason(*args, **kwargs)

        return new_func

    elif isinstance(reason, string_types):
        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter("always", DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                warnings.simplefilter("default", DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    else:
        raise TypeError(repr(type(reason)))
