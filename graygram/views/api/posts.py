# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from graygram import m
from graygram.exceptions import BadRequest
from graygram.exceptions import Conflict
from graygram.exceptions import Forbidden
from graygram.orm import db
from graygram.paging import next_url
from graygram.photo_uploader import InvalidImage
from graygram.renderers import render_json


view = Blueprint('api.posts', __name__, url_prefix='/posts')


@view.route('/<post_id>')
def get_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    return render_json(post)


@view.route('', methods=['POST'])
@login_required
def create_post():
    if 'photo' not in request.files:
        raise BadRequest(message="Missing parameter", field='photo')
    try:
        photo = m.Photo.upload(file=request.files['photo'])
    except InvalidImage:
        raise BadRequest(message="Invalid image", field='photo')

    message = request.values.get('message')

    post = m.Post()
    post.user = current_user
    post.photo = photo
    post.message = message
    db.session.add(post)
    db.session.commit()
    return render_json(post), 201


@view.route('/<post_id>', methods=['PUT', 'PATCH'])
@login_required
def update_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    if post.user != current_user:
        raise Forbidden()
    post.message = request.values.get('message')
    db.session.add(post)
    db.session.commit()
    return render_json(post)


@view.route('/<post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    if post.user != current_user:
        raise Forbidden()
    db.session.delete(post)
    db.session.commit()
    return render_json({})


@view.route('/<post_id>/likes')
def get_likes(post_id):
    post = m.Post.query.get_or_404(post_id)
    limit = request.values.get('limit', 30, type=int)
    offset = request.values.get('offset', 0, type=int)
    post_likes = m.PostLike.query \
        .filter_by(post=post) \
        .order_by(m.PostLike.liked_at.desc()) \
        .offset(offset) \
        .limit(limit)
    data = {
        'data': [post_like.serialize() for post_like in post_likes],
        'paging': None,
    }
    if limit + offset < m.Post.query.count():
        data['paging'] = {
            'next': next_url(limit=limit, offset=offset),
        }
    return render_json(data)


@view.route('/<post_id>/likes', methods=['POST'])
@login_required
def like_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    if post.is_liked:
        raise Conflict()
    post.is_liked = True
    db.session.add(post)
    db.session.commit()
    return render_json({}), 201


@view.route('/<post_id>/likes', methods=['DELETE'])
@login_required
def unlike_post(post_id):
    post = m.Post.query.get_or_404(post_id)
    if not post.is_liked:
        raise Conflict()
    post.is_liked = False
    db.session.add(post)
    db.session.commit()
    return render_json({})
