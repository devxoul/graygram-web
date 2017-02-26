import pytest

from clients import APIClient

from graygram import cache
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
    cache.clear()

    def teardown():
        db.session.close()
        for table in db.metadata.tables.keys():
            db.session.execute('DROP TABLE {}'.format(table))
        db.drop_all()
        cache.clear()
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
    from graygram.s3 import client

    def get_usercontent_bucket_name():
        execfile('config/test.cfg')
        return locals()['S3_USERCONTENT_BUCKET']

    bucket_name = get_usercontent_bucket_name()
    try:
        client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': 'ap-northeast-2',
        })
    except:
        pass

    def teardown():
        try:
            clear_bucket(bucket_name)
            client.delete_bucket(Bucket=bucket_name)
        except:
            pass
    request.addfinalizer(teardown)


def clear_bucket(bucket_name):
    from graygram.s3 import client
    r = client.list_objects(Bucket=bucket_name)
    objects = [dict(Key=content['Key']) for content in r['Contents']]
    client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
