"""
Portal default and base Flask configurations
"""

# pylint: disable=too-few-public-methods

import os


class BaseConfig(object):
    """
    Base Configuration for Flask. Applies to all applications using
    :class:`portal.factory.configure_app()`
    """

    ENV = None

    PROJECT = "{{cookiecutter.app_name|title}}"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    ADMINS = ['{{cookiecutter.email}}']

    INSTANCE_FOLDER_PATH = os.path.join(os.path.expanduser("~"), 'INSTANCE_FOLDER_PATH/')

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')

    DEBUG = False
    TESTING = False

    # Flask-Cache Settings
    CACHE_TYPE = 'memcached'  # Can be "memcached", "redis", etc.

    # Flask Debug-Toolbar Settings
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_NAME = 'application.db'
    DATABASE_PATH = os.path.join(INSTANCE_FOLDER_PATH, DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH)

    API_URL = "http://127.0.0.1:5000"


class DefaultConfig(BaseConfig):
    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class ProductionConfig(BaseConfig):
    """
    Configuration object from :class:`portal.config.BaseConfig` for
    production Flask apps. Applies to all applications using
    :method:`portal.factory.configure_app()`
    """

    ENV = 'prod'

    LOGLEVEL = 'INFO'

    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = 'mysql://'

    API_URL = ""


class TestConfig(BaseConfig):
    """
    Configuration object from :class:`portal.config.BaseConfig`
    Configuration for Flask. Applies to all applications using
    :method:`portal.factory.configure_app()`
    """
    SECRET_KEY = 'SUPERVERYSUPERSECRETTHATSSECRETLYASECRET'

    LOGLEVEL = "DEBUG"

    DEBUG = True
    TESTING = True

    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "redis"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class DevConfig(BaseConfig):
    ENV = "dev"
    SECRET_KEY = 'SUPERVERYSUPERSECRETTHATSSECRETLYASECRET'

    LOGLEVEL = "DEBUG"

    DEBUG = True
    TESTING = False

    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')

    ASSETS_DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    CACHE_TYPE = 'memcached'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_NAME = 'development.db'
    DATABASE_PATH = os.path.join(BaseConfig.PROJECT_ROOT, DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH)
