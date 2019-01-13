"""S3 backend"""

import gzip
import urllib

import boto3


class Backend:
    """Stone backend for writing to file"""
    def __init__(self, *args, **kwargs):
        self._bucket = kwargs.get('bucket')
        self._cache_control = kwargs.get('cache-control', '3600')
        # https://tools.ietf.org/html/rfc5646
        self._content_language = kwargs.get('content-language', 'en')
        self._metadata = kwargs.get('metadata', {})
        self._tags = kwargs.get('tags')
        self._prefix = kwargs.get('prefix', '')

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return str(tuple(self))

    def commit(self, page, *args, **kwargs):
        """Commit page to S3 bucket"""
        s3 = boto3.client("s3")

        try:
            tags = urllib.parse.urlencode(self._tags)
        except TypeError:
            tags = ''

        s3.put_object(
            Body=gzip.compress(page['content'].encode()),
            Bucket=self._bucket,
            Key=self._prefix + page['target'],
            ContentEncoding='gzip',
            ContentLanguage=self._content_language,
            ContentType='text/html',
            CacheControl=self._cache_control,
            Metadata=self._metadata,
            Tagging=tags)
