# -*- coding: utf-8 -*-

import pytest
import uuid

from graygram import m
from graygram.orm import db


def _create_fixture(topic, user):
    photo = m.Photo()
    photo.id = str(uuid.uuid4())
    photo.user = user
    photo.original_width = 1280
    photo.original_height = 1280
    db.session.add(photo)
    post = m.Post()
    post.user = user
    post.photo = photo
    post.message = 'It\'s {}!'.format(topic)
    db.session.add(post)
    db.session.commit()
    return post


@pytest.fixture
def post_tower_eiffel(request, user_ironman):
    return _create_fixture('tower_eiffel', user_ironman)


@pytest.fixture
def post_espresso(request, user_captain_america):
    return _create_fixture('espresso', user_captain_america)
