# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import login_user

from graygram import m
from graygram.crypto import bcrypt
from graygram.exceptions import BadRequest
from graygram.renderers import render_json


view = Blueprint('api.login', __name__, url_prefix='/login')


@view.route('/username', methods=['POST'])
def username():
    username = request.values.get('username')
    if not username:
        raise BadRequest(message="Missing parameter", field='username')

    password = request.values.get('password')
    if not password:
        raise BadRequest(message="Missing parameter", field='password')

    cred = m.Credential.query.filter_by(type='username', key=username).first()
    if not cred:
        raise BadRequest(message="User not registered", field='username')

    password_correct = bcrypt.check_password_hash(cred.value, password)
    if not password_correct:
        raise BadRequest(message="Wrong password", field='password')

    login_user(cred.user, remember=True)
    return render_json(cred.user)
