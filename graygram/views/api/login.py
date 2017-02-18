# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import login_user
from werkzeug.exceptions import BadRequest

from graygram import m
from graygram.crypto import bcrypt
from graygram.renderers import render_json


view = Blueprint('api.login', __name__, url_prefix='/login')


@view.route('/username', methods=['POST'])
def username():
    username = request.values.get('username')
    if not username:
        raise BadRequest("Missing parameter: 'username'")

    password = request.values.get('password')
    if not password:
        raise BadRequest("Missing parameter: 'password'")

    cred = m.Credential.query.filter_by(type='username', key=username).first()
    if not cred:
        raise BadRequest("User not registered")

    password_correct = bcrypt.check_password_hash(cred.value, password)
    if not password_correct:
        raise BadRequest("Wrong password")

    login_user(cred.user, remember=True)
    return render_json(cred.user)
