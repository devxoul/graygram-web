def test_join_failure_missing_username(api):
    r = api.post('/join/username', data={})
    assert r.status_code == 400
    assert 'username' in r.json['message']


def test_join_failure_missing_password(api):
    r = api.post('/join/username', data={
        'username': 'abc',
    })
    assert r.status_code == 400
    assert 'password' in r.json['message']


def test_join_failure_username_alread_exists(api, user_ironman):
    r = api.post('/join/username', data={
        'username': 'ironman',
        'password': 'secret',
    })
    assert r.status_code == 409
    assert 'already exists' in r.json['message']


def test_join_success(api):
    r = api.post('/join/username', data={
        'username': 'ironman',
        'password': 'password_ironman',
    })
    assert r.status_code == 200
