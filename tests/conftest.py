import pytest

from clients import APIClient

from graygram.app import create_app
from graygram.orm import db

from . import import_fixtures


import_fixtures()


@pytest.fixture
def app(request):
    app = create_app(config='config/test.cfg')
    ctx = app.app_context()
    ctx.push()
    db.create_all()

    def teardown():
        db.session.close()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def api(request, app):
    client = APIClient(app, app.response_class)
    client.subdomain = 'api'
    client.headers['Accept'] = 'application/json'
    return client


@pytest.fixture
def login(request, api):
    def _login(user):
        api.post('/login/username', data={
            'username': user.username,
            'password': 'password_' + user.username,
        })
    return _login
