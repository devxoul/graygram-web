#!/usr/bin/env python

from setuptools import setup

install_requires = [
    'boto3==1.4.4',
    'Flask-Bcrypt==0.7.1',
    'Flask-Login==0.4.0',
    'Flask-Migrate==2.0.2',
    'Flask-Script==2.0.5',
    'Flask-SQLAlchemy==2.1',
    'Flask==0.12',
    'gunicorn==19.6.0',
    'psycopg2==2.6.2',
    'pytz==2016.10',
    'redis==2.10.5',
    'wand==0.4.4',
]

setup(name='Graygram',
      version='0.1.0',
      description='Graygram',
      author='Suyeol Jeon',
      author_email='devxoul@gmail.com',
      url='https://github.com/devxoul/graygram-web',
      packages=['graygram'],
      install_requires=install_requires)
