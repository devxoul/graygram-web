# -*- coding: utf-8 -*-

from sqlalchemy.sql import functions as sqlfuncs

from graygram.orm import db


class PostLike(db.Model):
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    post = db.relationship('Post')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

    liked_at = db.Column(db.DateTime(timezone=True), nullable=False,
                         server_default=sqlfuncs.now())

    def serialize(self):
        return {
            'user': self.user,
            'liked_at': self.liked_at,
        }
