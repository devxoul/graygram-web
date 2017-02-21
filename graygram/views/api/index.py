# -*- coding: utf-8 -*-

from flask import Blueprint

from graygram.renderers import render_json


view = Blueprint('api.index', __name__)


@view.route('/')
def index():
    data = {
        'documentation_url': 'http://graygram.readthedocs.io/en/latest/',
        'ios_repo_url': 'https://github.com/devxoul/graygram-ios',
        'web_repo_url': 'https://github.com/devxoul/graygram-web',
    }
    return render_json(data)
