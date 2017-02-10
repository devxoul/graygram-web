# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from graygram import m
from graygram.paging import next_url
from graygram.renderers import render_json


view = Blueprint('api.feed', __name__, url_prefix='/feed')


@view.route('')
def feed():
    limit = request.values.get('limit', 30, type=int)
    offset = request.values.get('offset', 0, type=int)
    posts = m.Post.query \
        .order_by(m.Post.created_at.desc()) \
        .offset(offset) \
        .limit(limit)
    data = {
        'data': map(lambda post: post.serialize(), posts),
        'paging': None,
    }
    if limit + offset < m.Post.query.count():
        data['paging'] = {
            'next': next_url(limit=limit, offset=offset),
        }
    return render_json(data)
