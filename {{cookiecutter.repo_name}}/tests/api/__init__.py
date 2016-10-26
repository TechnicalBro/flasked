"""
tests.api
#########

api tests package
"""

from {{cookiecutter.app_name}}.api import create_app

from .. import {{cookiecutter.app_name}}AppTestCase
from {{cookiecutter.app_name}}.config import TestConfig


class PortalApiTestCase({{cookiecutter.app_name}}AppTestCase):
    def _create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        super(PortalApiTestCase, self).setUp()
