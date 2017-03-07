# -*- coding: utf-8 -*-

from botocore.exceptions import ClientError
from flask import Blueprint
from flask import current_app
from flask import redirect
from StringIO import StringIO

from graygram import photo_uploader
from graygram.exceptions import NotFound
from graygram.s3 import usercontent_bucket


def usercontent_url(*path_components):
    base_url = current_app.config['USERCONTENT_BASE_URL']
    return '/'.join([base_url] + list(path_components))


view = Blueprint('photos', __name__, url_prefix='/photos')


@view.route('/<path:photo_id>')
@view.route('/<path:photo_id>/original')
def get_original(photo_id):
    return redirect(usercontent_url(photo_id, 'original'))


@view.route('/<path:photo_id>/<int:width>x<int:height>')
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
        photo_uploader.upload(original,
                              photo_id=photo_id,
                              resize=(width, height))
    return redirect(usercontent_url(key))
