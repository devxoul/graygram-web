# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import current_user
from werkzeug.exceptions import BadRequest

from graygram import m
from graygram.orm import db
from graygram.photo_uploader import InvalidImage
from graygram.renderers import render_json


view = Blueprint('api.posts', __name__, url_prefix='/posts')


@view.route('/<post_id>')
def get_post(post_id):
    post = m.Post.get_or_404(post_id)
    return render_json(post)


@view.route('', methods=['POST'])
def create_post():
    if 'photo' not in request.files:
        raise BadRequest("Missing parameter: 'photo'")
    try:
        photo = m.Photo.upload(file=request.files['photo'])
    except InvalidImage:
        raise BadRequest('Invalid image')

    message = request.values.get('message')

    post = m.Post()
    post.user = current_user
    post.photo = photo
    post.message = message
    db.session.add(post)
    db.session.commit()
    return render_json(post)


@view.route('/<post_id>', methods=['PUT', 'PATCH'])
def update_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    post.message = request.values.get('message')
    db.session.add(post)
    db.session.commit()
    return render_json(post)
