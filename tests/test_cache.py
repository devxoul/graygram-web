import pytest

from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property

from graygram import cache


@pytest.fixture(autouse=True)
def change_model_base_class(request):
    cache.MODEL_BASE_CLASS = Model

    def teardown():
        from graygram.orm import db
        cache.MODEL_BASE_CLASS = db.Model
    request.addfinalizer(teardown)


class Model(object):
    pass


class Foo(Model):
    value = 10

    @hybrid_property
    @cache.memoize(timeout=300)
    def cached_value(self):
        return self.value

    @hybrid_method
    @cache.memoize(timeout=300)
    def cached_multiply(self, x):
        return self.value * x

    @cached_multiply.expression
    def cached_multiply(cls, x):
        return None


def test_hybrid_property(app):
    foo = Foo()
    assert foo.cached_value == 10

    foo.value = 20
    assert foo.cached_value == 10  # use cached value

    cache.delete_memoized('cached_value', foo)
    assert foo.cached_value == 20


def test_hybrid_method(app):
    foo = Foo()
    assert foo.cached_multiply(2) == 20

    foo.value = 20
    assert foo.cached_multiply(2) == 20  # use cached value

    cache.delete_memoized('cached_multiply', foo, 2)
    assert foo.cached_multiply(2) == 40
