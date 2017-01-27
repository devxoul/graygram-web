# -*- coding: utf-8 -*-

from sqlalchemy.sql import functions as sqlfuncs

from graygram.orm import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    photo_id = db.Column(db.String(36), db.ForeignKey('photo.id'))
    photo = db.relationship('Photo')

    message = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=sqlfuncs.now())

    def serialize(self):
        return {
            'id': self.id,
            'photo': self.photo,
            'message': self.message,
            'user': self.user,
            'created_at': self.created_at,
        }
