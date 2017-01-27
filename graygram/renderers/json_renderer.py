# -*- coding: utf-8 -*-

import json
import pytz

from datetime import datetime
from flask import Response
from flask_sqlalchemy import BaseQuery

from graygram.orm import db


def render_json(data=None):
    if not data:
        if isinstance(data, list):
            return Response('{"data": []}', mimetype='application/json')
        return Response('{}', mimetype='application/json')

    json_data = {}
    if isinstance(data, db.Model):
        json_data = data.serialize()

    elif isinstance(data, list) or isinstance(data, BaseQuery):
        json_data['data'] = []
        for v in data:
            if isinstance(v, dict):
                json_data['data'].append(v)
            elif isinstance(v, db.Model):
                json_data['data'].append(v.serialize())

    else:
        json_data = data

    json_data = traverse(json_data)
    return Response(json.dumps(json_data), mimetype='application/json')


def traverse(data):
    if isinstance(data, datetime):
        return data.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S%z')

    if isinstance(data, db.Model) and data.serialize:
        return traverse(data.serialize())

    if isinstance(data, dict):
        return {k: traverse(v) for k, v in data.iteritems()}

    if isinstance(data, list):
        return [traverse(d) for d in data]

    return data
