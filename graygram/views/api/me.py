# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_login import current_user
from flask_login import login_required

from graygram import m
from graygram.exceptions import BadRequest
from graygram.orm import db
from graygram.photo_uploader import InvalidImage
from graygram.renderers import render_json


view = Blueprint('api.users', __name__)


@view.route('/me')
@login_required
def get_me():
    return render_json(current_user.serialize())


@view.route('/me/photo', methods=['PUT'])
@login_required
def update_me_photo():
    if 'photo' not in request.files:
        raise BadRequest(message="Missing parameter", field='photo')
    try:
        photo = m.Photo.upload(file=request.files['photo'])
    except InvalidImage:
        raise BadRequest(message="Invalid image", field='photo')
    current_user.photo = photo
    db.session.add(current_user)
    db.session.commit()
    return render_json(current_user.serialize())


@view.route('/me/photo', methods=['DELETE'])
@login_required
def delete_me_photo():
    current_user.photo = None
    db.session.add(current_user)
    db.session.commit()
    return render_json(current_user.serialize())
