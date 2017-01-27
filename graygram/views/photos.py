# -*- coding: utf-8 -*-

from botocore.exceptions import ClientError
from flask import Blueprint
from flask import redirect
from flask import request
from StringIO import StringIO
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound

from graygram import m
from graygram import photo_uploader
from graygram.s3 import usercontent_bucket
from graygram.renderers import render_json


view = Blueprint('photos', __name__, url_prefix='/photos')


@view.route('', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        raise BadRequest("Missing parameter: 'file'")
    try:
        photo = m.Photo.upload(file=request.files['file'])
    except photo_uploader.InvalidImage:
        raise BadRequest("Invalid image")
    return render_json(photo)


@view.route('/<photo_id>')
@view.route('/<photo_id>/original')
def get_original(photo_id):
    return usercontent_bucket.url_for(photo_id + '/original')


@view.route('/<photo_id>/<int:width>x<int:height>')
def get_resized(photo_id, width, height):
    if width <= 0 or height <= 0 or width != height:
        raise NotFound()
    key = '{photo_id}/{width}x{height}'.format(photo_id=photo_id,
                                               width=width,
                                               height=height)
    try:
        usercontent_bucket.Object(key).get()  # check existing
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchKey':
            raise e
        original = StringIO()
        usercontent_bucket.download_fileobj(photo_id + '/original', original)
        original.seek(0)
        result = photo_uploader.upload(original,
                                       photo_id=photo_id,
                                       resize=(width, height))
        print result.id
    return redirect(usercontent_bucket.url_for(key))
