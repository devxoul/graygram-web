from graygram import m
from graygram.orm import db

from . import create_fixture

usernames = [
    'ironman',
    'captain_america',
]


def fixture_for(username):
    def fixture(request):
        password = 'password_' + username
        user = m.User.create(username=username, password=password)
        db.session.commit()
        return user
    return fixture

for username in usernames:
    fixture_name = 'user_{}'.format(username)
    create_fixture(__name__, fixture_name, fixture_for(username))
