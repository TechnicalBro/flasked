"""
Module containing all extensions used in
:method:`portal.factory.configure_extensions()`
"""
import flask
from flask.ext.cache import Cache
from flask.ext.cors import CORS
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Bundle, Environment
import time

db = SQLAlchemy()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
assets = Environment()
migrate = Migrate()
cors = CORS()
asset_bundles = {
    'css': Bundle(
        'public/css/FILE_NAME',
    ),
    'js': Bundle(
        'public/js/FILE_NAME',
    ),
    'fonts': Bundle(
        'public/fonts/FILE_NAME',
    )
}

assets.register('js', asset_bundles['js'])
assets.register('css', asset_bundles['css'])
assets.register('font', asset_bundles['fonts'])
