import json

from flask.testing import FlaskClient


class SubdomainClient(FlaskClient):

    subdomain = None

    def __init__(self, *args, **kwargs):
        self.subdomain = kwargs.get('subdomain')
        super(SubdomainClient, self).__init__(*args, **kwargs)

    def _get_http_host(self):
        if self.subdomain is None:
            return None
        try:
            server_name = self.application.config['SERVER_NAME']
        except KeyError:
            return None
        return self.subdomain + '.' + server_name

    def open(self, *args, **kwargs):
        kwargs.setdefault('environ_overrides', {})
        kwargs['environ_overrides']['HTTP_HOST'] = self._get_http_host()
        return super(SubdomainClient, self).open(*args, **kwargs)


class APIClient(SubdomainClient):

    headers = {}
    follow_redirects = True

    def __init__(self, *args, **kwargs):
        self.headers = kwargs.get('headers', self.headers)
        self.follow_redirects = kwargs.get('follow_redirects',
                                           self.follow_redirects)
        super(APIClient, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        kwargs['headers'] = self.headers
        kwargs['follow_redirects'] = self.follow_redirects
        response = super(APIClient, self).open(*args, **kwargs)
        if 'application/json' in self.headers.get('Accept'):
            response.json = json.loads(response.data)
        return response
