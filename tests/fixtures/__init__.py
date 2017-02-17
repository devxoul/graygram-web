import pytest
import sys


def create_fixture(module_name, fixture_name, f):
    pytest.fixture(f)
    f.__name__ = fixture_name
    setattr(sys.modules[module_name], fixture_name, f)
    return f
