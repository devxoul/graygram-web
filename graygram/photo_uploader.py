# -*- coding: utf-8 -*-

import uuid

from wand.exceptions import MissingDelegateError
from wand.image import Image

from graygram.s3 import usercontent_bucket


class PhotoUploaderException(Exception):
    pass


class InvalidImage(PhotoUploaderException):
    pass


class UploadResult(object):
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height


def upload(file, photo_id=None, resize=None):
    try:
        with Image(file=file) as image:
            if resize and len(resize) == 2:
                key = '{photo_id}/{width}x{height}'.format(photo_id=photo_id,
                                                           width=resize[0],
                                                           height=resize[1])
                image.resize(resize[0], resize[1])
            else:
                key = photo_id + '/original'
            photo_id = photo_id or str(uuid.uuid4())
            usercontent_bucket.put_object(
                ACL='public-read',
                Key=key,
                Body=image.make_blob(),
                ContentType='image/{}'.format(image.format.lower()),
                Metadata={
                    'width': str(image.size[0]),
                    'height': str(image.size[1]),
                }
            )
            return UploadResult(photo_id, image.size[0], image.size[1])

    except MissingDelegateError:
        raise InvalidImage()
