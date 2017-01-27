# -*- coding: utf-8 -*-

import boto3

from botocore.client import Config


class LazyBucket(object):
    _bucket = None

    def resolve(self, bucket):
        self._bucket = bucket

    def __getattr__(self, name):
        return getattr(self._bucket, name)

    def __setattr__(self, name, value):
        if name == '_bucket':
            super(LazyBucket, self).__setattr__(name, value)
        else:
            setattr(self._bucket, name, value)

    @property
    def baseurl(self):
        return 'https://s3.ap-northeast-2.amazonaws.com/' + self._bucket.name

    def url_for(self, key):
        return self.baseurl + '/' + key


usercontent_bucket = LazyBucket()


def init_app(app):
    config = Config(signature_version='s3v4')
    s3 = boto3.resource('s3', config=config)
    usercontent_bucket.resolve(s3.Bucket(app.config['S3_USERCONTENT_BUCKET']))
