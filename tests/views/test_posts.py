def test_get_post__failure__404(api):
    r = api.get('/posts/1')
    assert r.status_code == 404


def test_get_post__success(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.get('/posts/{}'.format(post_id))
    assert r.status_code == 200
    assert 'tower_eiffel' in r.json['message']


def test_create_post__failure__not_logged_in(api):
    r = api.post('/posts')
    assert r.status_code == 401


def test_create_post__failure__invalid_image(api, login, user_ironman):
    login(user_ironman)
    r = api.post('/posts', data={'photo': open('README.md')})
    assert r.status_code == 400
    assert r.json['error']['field'] == 'photo'
    assert 'invalid image' in r.json['error']['message'].lower()


def test_create_post__failure__missing_photo(api, login, user_ironman):
    login(user_ironman)
    r = api.post('/posts')
    assert r.status_code == 400
    assert r.json['error']['field'] == 'photo'
    assert 'missing' in r.json['error']['message'].lower()


def test_create_post__success__photo_only(api, login, user_ironman):
    login(user_ironman)
    r = api.post('/posts', data={
        'photo': open('./tests/images/tower_eiffel.jpg')
    })
    assert r.status_code == 201


def test_create_post__success__photo_and_message(api, login, user_ironman):
    login(user_ironman)
    r = api.post('/posts', data={
        'photo': open('./tests/images/tower_eiffel.jpg'),
        'message': 'I love Tower Eiffel',
    })
    assert r.status_code == 201


def test_update_post__failure__not_logged_in(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.put('/posts/{}'.format(post_id))
    assert r.status_code == 401


def test_update_post__failure__not_mine(api, login,
                                        post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    r = api.put('/posts/{}'.format(post_id))
    assert r.status_code == 403


def test_update_post__failure__404(api, login,
                                   post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id + 1
    r = api.put('/posts/{}'.format(post_id))
    assert r.status_code == 404


def test_update_post__success(api, login, post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id
    r = api.put('/posts/{}'.format(post_id), data={
        'message': 'New message :)',
    })
    assert r.status_code == 200
    assert r.json['message'] == 'New message :)'


def test_delete_post__failure__not_logged_in(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.delete('/posts/{}'.format(post_id))
    assert r.status_code == 401


def test_delete_post__failure__not_mine(api, login,
                                        post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    r = api.delete('/posts/{}'.format(post_id))
    assert r.status_code == 403


def test_delete_post__failure__404(api, login,
                                   post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id + 1
    r = api.delete('/posts/{}'.format(post_id))
    assert r.status_code == 404


def test_delete_post__success(api, login, post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id
    r = api.delete('/posts/{}'.format(post_id))
    assert r.status_code == 200


def test_get_post_likes__failure__404(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id + 1
    r = api.get('/posts/{}/likes'.format(post_id))
    assert r.status_code == 404


def test_get_post_likes__success__empty(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.get('/posts/{}/likes'.format(post_id))
    assert r.status_code == 200
    assert len(r.json['data']) == 0


def test_get_post_likes__success(api, login, post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    api.post('/posts/{}/likes'.format(post_id))
    r = api.get('/posts/{}/likes'.format(post_id))
    assert r.status_code == 200
    assert len(r.json['data']) == 1
    assert r.json['data'][0]['user']['username'] == 'ironman'


def test_like_post__failure__not_logged_in(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.post('/posts/{}/likes'.format(post_id))
    assert r.status_code == 401


def test_like_post__failure__404(api, login, post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id + 1
    r = api.post('/posts/{}/likes'.format(post_id))
    assert r.status_code == 404


def test_like_post__failure__conflict(api, login, post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    api.post('/posts/{}/likes'.format(post_id))
    r = api.post('/posts/{}/likes'.format(post_id))
    assert r.status_code == 409


def test_like_post__success__mine(api, login, post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id
    r = api.post('/posts/{}/likes'.format(post_id))
    assert r.status_code == 201
    r = api.get('/posts/{}'.format(post_id))
    assert r.json['like_count'] == 1


def test_like_post__success__others(api, login, post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    r = api.post('/posts/{}/likes'.format(post_id))
    assert r.status_code == 201
    r = api.get('/posts/{}'.format(post_id))
    assert r.json['like_count'] == 1


def test_unlike_post__failure__not_logged_in(api, post_tower_eiffel):
    post_id = post_tower_eiffel.id
    r = api.delete('/posts/{}/likes'.format(post_id))
    assert r.status_code == 401


def test_unlike_post__failure__404(api, login, post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id + 1
    r = api.delete('/posts/{}/likes'.format(post_id))
    assert r.status_code == 404


def test_unlike_post__failure__conflict(api, login,
                                        post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    r = api.delete('/posts/{}/likes'.format(post_id))
    assert r.status_code == 409


def test_unlike_post__success__mine(api, login,
                                    post_tower_eiffel, user_ironman):
    login(user_ironman)
    post_id = post_tower_eiffel.id
    api.post('/posts/{}/likes'.format(post_id))
    r = api.delete('/posts/{}/likes'.format(post_id))
    assert r.status_code == 200
    r = api.get('/posts/{}'.format(post_id))
    assert r.json['like_count'] == 0


def test_unlike_post__success__others(api, login,
                                      post_espresso, user_ironman):
    login(user_ironman)
    post_id = post_espresso.id
    api.post('/posts/{}/likes'.format(post_id))
    r = api.delete('/posts/{}/likes'.format(post_id))
    assert r.status_code == 200
    r = api.get('/posts/{}'.format(post_id))
    assert r.json['like_count'] == 0
