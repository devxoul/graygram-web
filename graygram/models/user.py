# -*- coding: utf-8 -*-

from flask_login import UserMixin
from sqlalchemy.sql import functions as sqlfuncs

from graygram import m
from graygram.crypto import bcrypt
from graygram.orm import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

    photo_id = db.Column(db.String(36), db.ForeignKey('photo.id'))
    photo = db.relationship('Photo', foreign_keys=[photo_id])

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=sqlfuncs.now())

    credentials = db.relationship('Credential', backref='user', lazy='dynamic')

    @classmethod
    def create(cls, username, password):
        user = m.User()
        user.username = username
        db.session.add(user)

        cred = m.Credential()
        cred.user = user
        cred.type = 'username'
        cred.key = username
        cred.value = bcrypt.generate_password_hash(password)
        db.session.add(cred)

        return user

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'photo': self.photo,
            'created_at': self.created_at,
        }
