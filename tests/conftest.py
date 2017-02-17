import pytest

from clients import APIClient

from graygram.app import create_app
from graygram.orm import db


@pytest.fixture
def app(request):
    app = create_app(config='config/test.cfg')
    ctx = app.app_context()
    ctx.push()
    db.create_all()

    def teardown():
        db.session.rollback()
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
