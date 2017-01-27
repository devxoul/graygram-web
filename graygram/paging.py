# -*- coding: utf-8 -*-

import urllib

from flask import request


def next_url(limit=None, offset=None):
    limit = limit or request.values.get('limit', 30, type=int)
    offset = offset or request.values.get('offset', 0, type=int)
    values = request.values.to_dict()
    values['offset'] = limit + offset
    return request.base_url + '?' + urllib.urlencode(values)
