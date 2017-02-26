# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from graygram import m
from graygram.paging import next_url
from graygram.renderers import render_json


view = Blueprint('api.feed', __name__, url_prefix='/feed')


@view.route('')
def feed():
    """
    **Example request**:

    .. sourcecode:: http

        GET /feed HTTP/1.1
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "data": [
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
            },
            {
              "message": "서울의 한 골목",
              "id": 13,
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
              "created_at": "2017-01-27T19:52:02+0000",
              "photo": {
                "id": "1e6833e2-f041-49be-9e4a-5691d084910d"
              }
            }
          ],
          "paging": {
            "next": "https://www.graygram.com/feed?limit=2&offset=2"
          },
        }

    :query limit:
    :query offset:
    :>json array data: Array of ``Post``
    :>json string paging.next: (Optional) Next page URL
    """

    limit = request.values.get('limit', 30, type=int)
    offset = request.values.get('offset', 0, type=int)
    posts = m.Post.query \
        .order_by(m.Post.created_at.desc()) \
        .offset(offset) \
        .limit(limit)
    data = {
        'data': [post.serialize() for post in posts],
        'paging': None,
    }
    if limit + offset < m.Post.query.count():
        data['paging'] = {
            'next': next_url(limit=limit, offset=offset),
        }
    return render_json(data)
