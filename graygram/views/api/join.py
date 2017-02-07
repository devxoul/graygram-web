# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Conflict

from graygram import m
from graygram.crypto import bcrypt
from graygram.orm import db
from graygram.renderers import render_json


view = Blueprint('join', __name__, url_prefix='/join')


@view.route('/username', methods=['POST'])
def username():
    username = request.values.get('username')
    if not username:
        raise BadRequest("Missing parameter: 'username'")

    password = request.values.get('password')
    if not password:
        raise BadRequest("Missing parameter: 'password'")

    cred = m.Credential.query.filter_by(type='username', key=username).first()
    if cred:
        raise Conflict("User '{}' already exists.".format(username))

    user = m.User()
    user.username = username
    db.session.add(user)

    cred = m.Credential()
    cred.user = user
    cred.type = 'username'
    cred.key = username
    cred.value = bcrypt.generate_password_hash(password)
    db.session.add(cred)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict("User '{}' already exists.".format(username))

    login_user(user)
    return render_json(user)
