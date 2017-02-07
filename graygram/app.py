# -*- coding: utf-8 -*-

import json
import os

from flask import Flask
from flask import request
from flask import Response
from werkzeug.exceptions import default_exceptions

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

    if not app.debug:
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

    return app


def register_blueprints(app):
    app.url_map.default_subdomain = 'www'
    for blueprint_name in blueprints:
        path = 'graygram.views.%s' % blueprint_name
        view = __import__(path, fromlist=[blueprint_name])
        blueprint = getattr(view, 'view')
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
    def errorhandler(err):
        accept = request.headers.get('Accept', '')
        if 'application/json' in accept:
            data = {
                'status': err.code,
                'name': err.name,
                'description': err.description
            }
            res = json.dumps(data)
            return Response(res, mimetype='application/json', status=err.code)
        else:
            html = "<h1>{0}: {1}</h1><p>{2}</p>".format(err.code, err.name,
                                                        err.description)
            return Response(html, status=err.code)

    for code in default_exceptions.iterkeys():
        app.register_error_handler(code, errorhandler)
