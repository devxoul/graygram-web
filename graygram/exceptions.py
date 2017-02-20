# -*- coding: utf-8 -*-

import json

from werkzeug._compat import text_type
from werkzeug.exceptions import HTTPException as _HTTPException


class HTTPException(_HTTPException):

    status_code = None
    message = None
    field = None
    response = None

    def __init__(self, message=None, field=None):
        self.message = message or self.name
        self.field = field

    @property
    def code(self):
        return self.status_code

    def get_accept(self, environ):
        if environ is None:
            return 'text/html'
        return environ.get('HTTP_ACCEPT', 'text/html')

    def get_headers(self, environ=None):
        accept = self.get_accept(environ)
        if 'application/json' in accept:
            return [('Content-Type', 'application/json')]
        else:
            return super(HTTPException, self).get_headers(environ)

    def get_body(self, environ=None):
        accept = self.get_accept(environ)
        if 'application/json' in accept:
            return text_type(self.get_json_body())
        else:
            return text_type(self.get_html_body())

    def get_json_body(self):
        data = {
            'error': {
                'message': self.message,
                'field': self.field,
            }
        }
        return json.dumps(data)

    def get_html_body(self):
        if self.field is not None:
            template = '<h1>{status_code} {name}</h1><p>{field}: {message}</p>'
        else:
            template = '<h1>{status_code} {name}</h1><p>{message}</p>'
        return template.format(status_code=self.status_code,
                               name=self.name,
                               field=self.field,
                               message=self.message)


class BadRequest(HTTPException):
    status_code = 400


class Unauthorized(HTTPException):
    status_code = 401


class Forbidden(HTTPException):
    status_code = 403


class NotFound(HTTPException):
    status_code = 404


class MethodNotAllowed(HTTPException):
    status_code = 405


class NotAcceptable(HTTPException):
    status_code = 406


class RequestTimeout(HTTPException):
    status_code = 408


class Conflict(HTTPException):
    status_code = 409


class Gone(HTTPException):
    status_code = 410


class LengthRequired(HTTPException):
    status_code = 411


class PreconditionFailed(HTTPException):
    status_code = 412


class RequestEntityTooLarge(HTTPException):
    status_code = 413


class RequestURITooLarge(HTTPException):
    status_code = 414


class UnsupportedMediaType(HTTPException):
    status_code = 415


class RequestedRangeNotSatisfiable(HTTPException):
    status_code = 416


class ExpectationFailed(HTTPException):
    status_code = 417


class ImATeapot(HTTPException):
    status_code = 418


class UnprocessableEntity(HTTPException):
    status_code = 422


class Locked(HTTPException):
    status_code = 423


class PreconditionRequired(HTTPException):
    status_code = 428


class TooManyRequests(HTTPException):
    status_code = 429


class RequestHeaderFieldsTooLarge(HTTPException):
    status_code = 431


class UnavailableForLegalReasons(HTTPException):
    status_code = 451


class InternalServerError(HTTPException):
    status_code = 500


class NotImplemented(HTTPException):
    status_code = 501


class BadGateway(HTTPException):
    status_code = 502


class ServiceUnavailable(HTTPException):
    status_code = 503


class GatewayTimeout(HTTPException):
    status_code = 504


class HTTPVersionNotSupported(HTTPException):
    status_code = 505
