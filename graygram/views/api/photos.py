# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from werkzeug.exceptions import BadRequest

from graygram import m
from graygram import photo_uploader
from graygram.renderers import render_json


view = Blueprint('api.photos', __name__, url_prefix='/photos')


@view.route('', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        raise BadRequest("Missing parameter: 'file'")
    try:
        photo = m.Photo.upload(file=request.files['file'])
    except photo_uploader.InvalidImage:
        raise BadRequest("Invalid image")
    return render_json(photo)
