# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_login import logout_user

from graygram.renderers import render_json


view = Blueprint('api.logout', __name__)


@view.route('/logout')
def logout():
    """Logout from the current session.

    **Example request**:

    .. sourcecode:: http

        GET /logout HTTP/1.1
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {}
    """

    logout_user()
    return render_json({})
