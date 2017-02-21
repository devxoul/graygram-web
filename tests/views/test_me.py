from graygram.s3 import usercontent_bucket


def test_get_me_failure__not_logged_in(api):
    r = api.get('/me')
    assert r.status_code == 401


def test_get_me_success(api, login, user_ironman):
    login(user_ironman)
    r = api.get('/me')
    assert r.status_code == 200
    assert r.json['username'] == 'ironman'


def test_update_profile_photo__failure_not_logged_in(api, login):
    r = api.put('/me/photo')
    assert r.status_code == 401


def test_update_profile_photo__failure_no_file(api, login, user_ironman):
    login(user_ironman)
    r = api.put('/me/photo')
    assert r.status_code == 400
    assert r.json['error']['field'] == 'photo'
    assert 'missing' in r.json['error']['message'].lower()


def test_update_profile_photo__success(api, login, user_ironman):
    login(user_ironman)
    r = api.put('/me/photo', data={
        'photo': open('./tests/images/ironman.png'),
    })
    assert r.status_code == 200
    key = r.json['photo']['id'] + '/original'
    assert usercontent_bucket.object_exists(key)


def test_delete_profile_photo__failure_not_logged_in(api, login):
    r = api.delete('/me/photo')
    assert r.status_code == 401


def test_delete_profile_photo__success(api, login, user_ironman):
    login(user_ironman)
    r = api.put('/me/photo', data={
        'photo': open('./tests/images/ironman.png'),
    })
    r = api.delete('/me/photo')
    assert r.status_code == 200
    assert r.json['photo'] is None
