# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import redirect
from flask import request
from werkzeug.exceptions import default_exceptions

from graygram import exceptions
from graygram import s3
from graygram.crypto import bcrypt
from graygram.orm import db
from graygram.views import blueprints


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_pyfile(os.path.abspath(config))
    else:
        app.config.from_envvar('CONFIG')

    if not app.debug and not app.testing:
        from flask.ext.sslify import SSLify
        SSLify(app, permanent=True)
        from raven.contrib.flask import Sentry
        Sentry(app)

    install_errorhandler(app)
    register_blueprints(app)

    db.init_app(app)
    bcrypt.init_app(app)
    s3.init_app(app)
    init_extensions(app)

    @app.route('/')
    def index():
        return redirect('https://github.com/devxoul/graygram-ios')

    return app


def register_blueprints(app):
    app.url_map.default_subdomain = 'www'
    for blueprint_name in blueprints:
        path = 'graygram.views.%s' % blueprint_name
        view = __import__(path, fromlist=[blueprint_name])
        blueprint = getattr(view, 'view')
        if blueprint_name.startswith('api.'):
            blueprint.subdomain = 'api'
        app.register_blueprint(blueprint)


def init_extensions(app):
    from flask_login import LoginManager
    from flask_migrate import Migrate

    login = LoginManager(app=app)

    @login.user_loader
    def load_user(user_id):
        from graygram.models.user import User
        return User.query.get(user_id)

    Migrate(app, db)


def install_errorhandler(app):
    def errorhandler(error):
        if not isinstance(error, exceptions.HTTPException):
            error = getattr(exceptions, error.__class__.__name__)()
        return error.get_response(request.environ)

    for code in default_exceptions.iterkeys():
        app.register_error_handler(code, errorhandler)
