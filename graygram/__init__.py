# -*- coding: utf-8 -*-

from sqlalchemy.util import dependencies


class ModelImporter(object):

    _unresolved = {}

    def __init__(self):
        from graygram.models import classes

        for class_ in classes:
            components = class_.split('.')
            name = components[-1]
            path = 'graygram.models.%s' % components[-2]
            importer = dependencies._importlater(path, name)
            self._unresolved[name] = importer

    def resolve_all(self):
        for name in self._unresolved.keys():
            importer = self._unresolved[name]
            importer._resolve()
            setattr(self, name, importer.module)
            del self._unresolved[name]

m = ModelImporter()
m.resolve_all()
