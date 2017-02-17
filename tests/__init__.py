import os
import sys


def import_fixtures():
    module_names = _get_fixture_module_names()
    for module_name in module_names:
        _import_fixtures_from(module_name)


def _get_fixture_module_names():
    module_names = []
    for filename in os.listdir('./tests/fixtures'):
        if not filename.startswith('_') and filename.endswith('.py'):
            module_name = filename.split('.')[0]
            module_names.append(module_name)
    return module_names


def _import_fixtures_from(module_name):
    path = 'tests.fixtures.{}'.format(module_name)
    __import__(path, fromlist=[module_name])
    fixtures = _get_fixtures_from(path)
    for name, fixture in fixtures:
        setattr(sys.modules['tests.conftest'], name, fixture)


def _get_fixtures_from(name):
    fixtures = []
    for key in dir(sys.modules[name]):
        if key.startswith('_'):
            continue
        value = getattr(sys.modules[name], key)
        try:
            getattr(value, '_pytestfixturefunction')
            fixtures.append((key, value))
        except AttributeError:
            continue
    return fixtures
