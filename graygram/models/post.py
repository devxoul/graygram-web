# -*- coding: utf-8 -*-

from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import functions as sqlfuncs

from graygram import cache
from graygram import m
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

    def __repr__(self):
        return '<Post %d>' % self.id

    @hybrid_property
    @cache.memoize(timeout=300)
    def like_count(self):
        return m.PostLike.query.filter_by(post_id=self.id).count()

    @like_count.expression
    def like_count(cls):
        return select([sqlfuncs.count(m.PostLike.user_id)]) \
            .where(m.PostLike.post_id == cls.id) \
            .label('count')

    @hybrid_method
    @cache.memoize(timeout=300)
    def is_liked_by(self, user):
        post_like = m.PostLike.query \
            .filter_by(user_id=user.id, post_id=self.id) \
            .first()
        return post_like is not None

    @is_liked_by.expression
    def is_liked_by(cls, user):
        return m.PostLike.query \
            .filter_by(user_id=user.id, post_id=cls.id) \
            .exists()

    @hybrid_property
    def is_liked(self):
        from flask_login import current_user
        if not current_user.is_authenticated:
            return False
        return self.is_liked_by(current_user)

    @is_liked.expression
    def is_liked(cls):
        from flask_login import current_user
        if not current_user.is_authenticated:
            return False
        return cls.is_liked_by(current_user)

    @is_liked.setter
    def is_liked(self, value):
        from flask_login import current_user
        if not current_user.is_authenticated:
            return
        if value:
            post_like = m.PostLike(user_id=current_user.id, post_id=self.id)
            db.session.add(post_like)
        else:
            post_like = m.PostLike.query \
                .filter_by(user_id=current_user.id, post_id=self.id) \
                .first()
            if post_like:
                db.session.delete(post_like)
        cache.delete_memoized('is_liked_by', self, current_user)
        cache.delete_memoized('like_count', self)

    def serialize(self):
        return {
            'id': self.id,
            'photo': self.photo,
            'message': self.message,
            'user': self.user,
            'created_at': self.created_at,
            'like_count': self.like_count,
            'is_liked': self.is_liked,
        }
