import pytest

from graygram import m
from graygram.orm import db


@pytest.fixture
def user_ironman(request):
    user = m.User.create(username='ironman', password='password_ironman')
    db.session.commit()
    return user


def test_login_failure_missing_username(api):
    r = api.post('/login/username', data={})
    assert r.status_code == 400
    assert 'username' in r.json['message']


def test_login_failure_missing_password(api):
    r = api.post('/login/username', data={
        'username': 'abc',
    })
    assert r.status_code == 400
    assert 'password' in r.json['message']


def test_login_failure_unregistered_user(api):
    r = api.post('/login/username', data={
        'username': 'unknown',
        'password': 'secret',
    })
    assert r.status_code == 400
    assert 'not registered' in r.json['message']


def test_login_success(api, user_ironman):
    r = api.post('/login/username', data={
        'username': 'ironman',
        'password': 'password_ironman',
    })
    assert r.status_code == 200
