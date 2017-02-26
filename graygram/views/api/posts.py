# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from graygram import cache
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
    """Get a single post.

    **Example JSON response**:

    .. sourcecode:: json

        {
          "message": "생 마르탱 운하에서 본 할머니와 할아버지",
          "id": 14,
          "is_liked": false,
          "like_count": 0,
          "user": {
            "created_at": "2017-02-07T09:23:13+0000",
            "photo": {
              "id": "d7394923-cf39-4c78-891a-8714eb615ea7"
            },
            "username": "devxoul",
            "id": 1
          },
          "created_at": "2017-01-27T19:52:32+0000",
          "photo": {
            "id": "69e892b4-7dbd-403c-92fc-07f199c2be35"
          }
        }

    :>json int id:
    :>json Photo photo:
    :>json string message: A message (Optional)
    :>json User user: Post author
    :>json date created_at:

    :statuscode 200: OK
    :statuscode 404: There's no post
    """

    post = m.Post.query.get_or_404(post_id)
    return render_json(post)


@view.route('', methods=['POST'])
@login_required
def create_post():
    """Create a post

    **Example JSON response**:

    .. sourcecode:: json

        {
          "message": "생 마르탱 운하에서 본 할머니와 할아버지",
          "id": 14,
          "is_liked": false,
          "like_count": 0,
          "user": {
            "created_at": "2017-02-07T09:23:13+0000",
            "photo": {
              "id": "d7394923-cf39-4c78-891a-8714eb615ea7"
            },
            "username": "devxoul",
            "id": 1
          },
          "created_at": "2017-01-27T19:52:32+0000",
          "photo": {
            "id": "69e892b4-7dbd-403c-92fc-07f199c2be35"
          }
        }

    :form photo: An image file
    :form message: A message (Optional)
    :statuscode 201: Created
    :statuscode 400: Required parameter is missing or invalid
    :statuscode 401: Not authorized
    """

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
    """Edit the post

    **Example JSON response**:

    .. sourcecode:: json

        {
          "message": "생 마르탱 운하에서 본 할머니와 할아버지",
          "id": 14,
          "is_liked": false,
          "like_count": 0,
          "user": {
            "created_at": "2017-02-07T09:23:13+0000",
            "photo": {
              "id": "d7394923-cf39-4c78-891a-8714eb615ea7"
            },
            "username": "devxoul",
            "id": 1
          },
          "created_at": "2017-01-27T19:52:32+0000",
          "photo": {
            "id": "69e892b4-7dbd-403c-92fc-07f199c2be35"
          }
        }

    :form message: New message (Optional)
    :statuscode 200: OK
    :statuscode 401: Not authorized
    :statuscode 403: No permission
    """
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
    """ Delete the post

    **Example JSON response**:

    .. sourcecode:: json

        {}

    :statuscode 200: Deleted
    :statuscode 401: Not authorized
    :statuscode 403: No permission
    """
    post = m.Post.query.get_or_404(post_id)
    if post.user != current_user:
        raise Forbidden()
    db.session.delete(post)
    db.session.commit()
    return render_json({})


@view.route('/<post_id>/likes')
def get_likes(post_id):
    """Get users who like the post

    **Example JSON response**:

    .. sorucecode:: json

        {
          "data": [
            {
              "username": "devxoul",
              "photo": null,
              "created_at": "2017-02-21T16:59:35+0000",
              "id": 1
            }
          ],
          "paging": {
            "next": null
          }
        }

    :statuscode 200: OK
    :statuscode 404: There's no post
    """
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
    """Like the post

    **Example JSON response**:

    .. sourcecode:: json

        {}

    :statuscode 201: Liked
    :statuscode 401: Not authorized
    :statuscode 409: Already liked
    """
    post = m.Post.query.get_or_404(post_id)
    cache.delete_memoized('is_liked_by', post, current_user)
    if post.is_liked:
        raise Conflict()
    post.is_liked = True
    db.session.add(post)
    db.session.commit()
    return render_json({}), 201


@view.route('/<post_id>/likes', methods=['DELETE'])
@login_required
def unlike_post(post_id):
    """Unlike the post

    **Example JSON response**:

    .. sourcecode:: json

        {}

    :statuscode 200: Unliked
    :statuscode 401: Not authorized
    :statuscode 409: Already unliked
    """
    post = m.Post.query.get_or_404(post_id)
    cache.delete_memoized('is_liked_by', post, current_user)
    if not post.is_liked:
        raise Conflict()
    post.is_liked = False
    db.session.add(post)
    db.session.commit()
    return render_json({})
