# -*- coding: utf-8 -*-

from flask_login import current_user

from graygram import m
from graygram import photo_uploader
from graygram.orm import db


class Photo(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # uuid
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])
    original_width = db.Column(db.Integer)
    original_height = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'original_width': self.original_width,
            'original_height': self.original_height,
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
