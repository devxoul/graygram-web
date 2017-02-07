# -*- coding: utf-8 -*-

import os

from flask import Blueprint


view = Blueprint('letsencrypt', __name__)


@view.route('/.well-known/acme-challenge/<key>', subdomain='')
@view.route('/.well-known/acme-challenge/<key>', subdomain='www')
@view.route('/.well-known/acme-challenge/<key>', subdomain='api')
def acme_challenge(key):
    return key + '.' + os.environ['ACME_CHALLENGE']
