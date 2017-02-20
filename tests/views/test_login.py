def test_login_failure_missing_username(api):
    r = api.post('/login/username', data={})
    assert r.status_code == 400
    assert r.json['error']['field'] == 'username'
    assert 'missing' in r.json['error']['message'].lower()


def test_login_failure_missing_password(api):
    r = api.post('/login/username', data={
        'username': 'abc',
    })
    assert r.status_code == 400
    assert r.json['error']['field'] == 'password'
    assert 'missing' in r.json['error']['message'].lower()


def test_login_failure_unregistered_user(api):
    r = api.post('/login/username', data={
        'username': 'unknown',
        'password': 'secret',
    })
    assert r.status_code == 400
    assert r.json['error']['field'] == 'username'
    assert 'not registered' in r.json['error']['message'].lower()


def test_login_success(api, user_ironman):
    r = api.post('/login/username', data={
        'username': 'ironman',
        'password': 'password_ironman',
    })
    assert r.status_code == 200
