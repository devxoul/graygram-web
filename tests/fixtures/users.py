import pytest

from graygram import m
from graygram.orm import db


@pytest.fixture
def user_ironman(request):
    user = m.User.create(username='ironman', password='password_ironman')
    db.session.commit()
    return user


@pytest.fixture
def user_captain_america(request):
    user = m.User.create(username='captain_america',
                         password='password_captain_america')
    db.session.commit()
    return user
