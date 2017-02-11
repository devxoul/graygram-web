# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import Response
from flask_login import logout_user


view = Blueprint('api.logout', __name__)


@view.route('/logout')
def logout():
    logout_user()
    return Response()
