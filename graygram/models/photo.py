# -*- coding: utf-8 -*-

from flask_login import current_user

from graygram import m
from graygram import photo_uploader
from graygram.s3 import usercontent_bucket
from graygram.orm import db


PHOTO_SIZES = {
    'hd': 640,
    'large': 320,
    'medium': 200,
    'thumbnail': 128,
    'small': 64,
    'tiny': 40,
}


class Photo(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # uuid
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    original_width = db.Column(db.Integer)
    original_height = db.Column(db.Integer)

    def serialize(self):
        url = {}
        for name, size in PHOTO_SIZES.iteritems():
            key = '{id}/{size}x{size}'.format(id=self.id, size=size)
            url[name] = usercontent_bucket.url_for(key)
        return {
            'original_width': self.original_width,
            'original_height': self.original_height,
            'url': url,
        }

    @classmethod
    def upload(cls, file):
        result = photo_uploader.upload(file)
        photo = m.Photo()
        photo.id = result.id
        photo.user = current_user
        photo.original_width = result.width
        photo.original_height = result.height
        db.session.add(photo)
        db.session.commit()
        return photo
