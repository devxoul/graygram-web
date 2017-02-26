# -*- coding: utf-8 -*-

from sqlalchemy.sql import functions as sqlfuncs

from graygram.orm import db


class Credential(db.Model):

    TYPES = frozenset(['username', 'admin'])

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,
                        index=True)
    type = db.Column(db.ENUM(*TYPES, name='credential_types'), nullable=False)

    #: `username`: username
    #: `admin`: email
    key = db.Column(db.String(255), nullable=False, unique=True)

    #: `username`: bcrypt password
    #: `admin`: None
    value = db.Column(db.String(255))

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=sqlfuncs.now())
