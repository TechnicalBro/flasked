import time

"""
This Portal utils module contains methods and functions
that are _not_ related to the MSTV (Model-Service-Template-View)
functionality of the application. Methods defined here are for
generic functionality of the controller itself, like where to
store data related to the installed application, how to format
dates, or how to create directories. Any thing above these
kinds of use cases should be defined in the Celery and/or
Service Layer of the application.
"""

# pylint: disable=too-few-public-methods

# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from datetime import timedelta

import os
import json
import uuid
import logging
import pprint
from functools import wraps, update_wrapper

from .exceptions import {{cookiecutter.app_name|title}}Error
from .compat import basestring

LOGGER = logging.getLogger(__name__)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def parse_date(datestr="", format="%Y-%m-%d"):
    from datetime import datetime

    if not datestr:
        return datetime.today().date()
    return datetime.strptime(datestr, format).date()


def make_dir(dir_path):
    """Function for making directories"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        LOGGER.debug('Creating directory - %s', dir_path)
    except PermissionError as e:
        LOGGER.exception('Unable to create directory! - %s', dir_path)
        raise e


def make_config_directories(config_obj):
    """
    Used by the factory to create the configuration-specific directories
    :param config_obj: Configuration Object
    :return: Does not return.
    """
    make_dir(config_obj.INSTANCE_FOLDER_PATH)
    make_dir(config_obj.LOG_FOLDER)


def attempt_token_auth(auth_header):
    """
    Asserts that the given auth_header matches the SECRET_KEY defined in the Flask app context

    :param str auth_header: Header payload stripped from the request
    """
    try:
        assert auth_header == 'Token {0}'.format(current_app.config['SECRET_KEY'])
    except AssertionError:
        raise PermissionError


def auth_token(func):
    """
    Decorator to place in a view-layer function. Will authenticate a token with the
    :class:`flask.request` context (using the headers)
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        """
        Wrapper for decorated function
        """
        LOGGER.info('Received request from IP - %s', request.environ.get('REMOTE_ADDR'))
        try:
            attempt_token_auth(request.environ.get('HTTP_AUTHORIZATION'))
        except PermissionError:
            LOGGER.error('Authorization failed for token %s',
                         request.environ.get('HTTP_AUTHORIZATION'))
            raise {{cookiecutter.app_name|title}}Error
            Error('Authorization failed')
        else:
            LOGGER.info('Successfully authenticated token')
        return func(*args, **kwargs)

    return func_wrapper


class CerberusValidate(object):
    """
    Decorator to validate request parameters against a given Cerberus schema
    """

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            """
            Wrapper for decorated function
            """
            LOGGER.info('Validating params with `%s`', self.schema.__name__)
            LOGGER.debug('Params - \n--ARGS--\n%s\n--KWARGS--\n%s', args, kwargs)
            v = self.schema()
            if v.validate(kwargs):
                LOGGER.debug('Successfully validated params')
                return func(*args, **kwargs)
            else:
                LOGGER.error('Failed to validate params - \n%s', v.errors)
                raise {{cookiecutter.app_name|title}}Error
                Error(v.errors, 500)

        return func_wrapper


def calc_progress(completed_count, total_count):
    """
    Calculate the percentage progress and estimated remaining time based on
    the current number of items completed of the total.

    Returns ``percentage_complete``.
    """

    if total_count is 0:
        return 0

    return 100 * float(completed_count) / float(total_count)


def expose_inner_class(cls):
    # get types of classes
    class classtypes:
        pass

    classtypes = (type, type(classtypes))

    # get names of all public names in outer class
    directory = [n for n in dir(cls) if not n.startswith("_")]

    # get names of all non-callable attributes of outer class
    attributes = [n for n in directory if not callable(getattr(cls, n))]

    # get names of all inner classes
    innerclasses = [n for n in directory if isinstance(getattr(cls, n), classtypes)]

    # copy attributes from outer to inner classes (don't overwrite)
    for c in innerclasses:
        c = getattr(cls, c)
        for a in attributes:
            if not hasattr(c, a):
                setattr(c, a, getattr(cls, a))

    return cls


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
