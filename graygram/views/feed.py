# -*- coding: utf-8 -*-

from flask import Blueprint

from graygram import m
from graygram.renderers import render_json


view = Blueprint('feed', __name__, url_prefix='/feed')


@view.route('')
def feed():
    posts = m.Post.query.all()
    return render_json(posts)
