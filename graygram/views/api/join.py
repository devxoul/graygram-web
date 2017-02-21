# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import login_user
from sqlalchemy.exc import IntegrityError

from graygram import m
from graygram.exceptions import BadRequest
from graygram.exceptions import Conflict
from graygram.orm import db
from graygram.renderers import render_json


view = Blueprint('api.join', __name__, url_prefix='/join')


@view.route('/username', methods=['POST'])
def username():
    """Create a new user with username and password.

    **Example request**:

    .. sourcecode:: http

        POST /join/username HTTP/1.1
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json

        {
          "username": "devxoul",
          "photo": null,
          "created_at": "2017-02-21T16:59:35+0000",
          "id": 1
        }

    :form username: Username of the user
    :form password: Password of the user
    :statuscode 201: Succeeded to create a new user
    :statuscode 400: Missing or wrong parameters
    :statuscode 409: User already exists
    """

    username = request.values.get('username')
    if not username:
        raise BadRequest(message="Missing parameter", field='username')

    password = request.values.get('password')
    if not password:
        raise BadRequest(message="Missing parameter", field='password')

    cred = m.Credential.query.filter_by(type='username', key=username).first()
    if cred:
        raise Conflict(message="User '{}' already exists.".format(username),
                       field='username')

    user = m.User.create(username=username, password=password)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="User '{}' already exists.".format(username),
                       field='username')

    login_user(user, remember=True)
    return render_json(user), 201
