# -*- coding: utf-8 -*-

from flask import current_app
from flask_migrate import MigrateCommand
from flask_script import Manager

from graygram import m
from graygram.app import create_app
from graygram.orm import db


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=True)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return {
        'app': current_app,
        'db': db,
        'm': m,
    }


if __name__ == '__main__':
    manager.run()
