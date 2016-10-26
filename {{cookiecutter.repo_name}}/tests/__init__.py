"""
tests
#####

tests package
"""

from unittest import TestCase

from .utils import FlaskTestCaseMixin

class {{cookiecutter.app_name}}TestCase(TestCase):
    pass


class {{cookiecutter.app_name}}AppTestCase(FlaskTestCaseMixin, {{cookiecutter.app_name}}TestCase):
    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        pass

    def setUp(self):
        super({{cookiecutter.app_name}}AppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        from {{cookiecutter.app_name}}.extensions import db

        db.app = self.app
        db.drop_all()
        db.create_all()

        self.db = db

        self._create_fixtures()

    def tearDown(self):
        super({{cookiecutter.app_name}}AppTestCase, self).tearDown()
        self.db.session.close()
        self.db.drop_all()
        self.app_context.pop()