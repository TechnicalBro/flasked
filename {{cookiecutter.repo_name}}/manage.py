#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
from glob import glob
from subprocess import call

import os
from flask_migrate import MigrateCommand, Migrate

from flask_script import Command, Manager, Option, Shell

from flask_script.commands import Clean, ShowUrls

from {{cookiecutter.app_name}}.api import create_app
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.config import ProductionConfig, DevConfig

CONFIG = DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app(settings_override=CONFIG)

manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and the User model by default."""
    return {
        'app': app,
        'db': db,
    }


@manager.command
def init_db():
    db.create_all()


@manager.command
def test():
    """Run the tests."""
    import pytest

    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


class Lint(Command):
    """Lint and check code style with flake8 and isort."""

    def get_options(self):
        """Command line options."""
        return (
            Option('-f', '--fix-imports', action='store_true', dest='fix_imports', default=False,
                   help='Fix imports using isort, before linting'),
        )

    def run(self, fix_imports):
        """Run command."""
        skip = ['requirements']
        root_files = glob('*.py')
        root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
        files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

        def execute_tool(description, *args):
            """Execute a checking tool with its arguments."""
            command_line = list(args) + files_and_directories
            print('{}: {}'.format(description, ' '.join(command_line)))
            rv = call(command_line)
            if rv is not 0:
                exit(rv)

        if fix_imports:
            execute_tool('Fixing import order', 'isort', '-rc')
        execute_tool('Checking code style', 'flake8')


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('lint', Lint())

if __name__ == '__main__':
    manager.run()
