import inspect

from flask_cache import Cache

from graygram.orm import db


MODEL_BASE_CLASS = db.Model
cache = Cache()


def init_app(app):
    cache.init_app(app)


def cached(*args, **kwargs):
    return cache.memoize(*args, **kwargs)


def memoize(*args, **kwargs):
    return cache.memoize(*args, **kwargs)


def delete_memoized(*args, **kwargs):
    if len(args) >= 2 and isinstance(args[1], MODEL_BASE_CLASS):
        return delete_memoized_hybrid(*args)
    else:
        return cache.delete_memoized(*args, **kwargs)


def delete_memoized_hybrid(name, obj, *args):
    f = getattr(type(obj), name)
    if not callable(f):
        f = f.fget
    if inspect.ismethod(f):  # hybrid_method
        f = getattr(obj, name)
    return cache.delete_memoized(f, obj, *args)


def clear(*args, **kwargs):
    return cache.clear()
