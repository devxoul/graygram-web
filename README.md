# Graygram

[![Build Status](https://travis-ci.org/devxoul/graygram-web.svg?branch=master)](https://travis-ci.org/devxoul/graygram-web)
[![Documentation Status](https://readthedocs.org/projects/graygram-web/badge/?version=latest)](http://graygram-web.readthedocs.io/en/latest/?badge=latest)

The backend server application for [Graygram](https://www.graygram.com). Written in Python 2.7 and Flask.

* [Documentation](http://graygram-web.readthedocs.io/en/latest/)
* [Graygram for iOS](https://github.com/devxoul/graygram-ios)

## Development

```console
$ python setup.py develop
$ python manage.py -c YOUR_CONFIGURATION_FILE db upgrade
$ python manage.py -c YOUR_CONFIGURATION_FILE runserver
```

Graygram uses subdomain for its API host. I'd recommend you to add following to your /etc/hosts file.

```
127.0.0.1    graygram.local
127.0.0.1    www.graygram.local
127.0.0.1    api.graygram.local
127.0.0.1    usercontent.graygram.local
```

Then you'll be able to send a request to your local server: `http://api.graygram.local:5000`

## Testing

```console
$ pytest
```

## Documentation

```console
$ cd docs
$ make clean html
$ open build/html/index.html
```

## Deployment

Graygram is being served on Heroku.

## License

Graygram is under MIT license. See the [LICENSE](LICENSE) file for more info.
