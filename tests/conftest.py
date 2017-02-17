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
        for table in db.metadata.tables.keys():
            db.session.execute('DROP TABLE {}'.format(table))
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


@pytest.fixture(scope='session', autouse=True)
def s3(request):
    import boto3
    from botocore.client import Config

    def get_usercontent_bucket_name():
        execfile('config/test.cfg')
        return locals()['S3_USERCONTENT_BUCKET']

    bucket_name = get_usercontent_bucket_name()
    config = Config(signature_version='s3v4')
    s3 = boto3.resource('s3', config=config, region_name='ap-northeast-1')
    try:
        s3.create_bucket(Bucket=bucket_name)
    except:
        pass
