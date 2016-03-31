'''
Aliyun OSS Stroage Backends
'''
import os
import oss2  # aliyun oss sdk
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


def get_aliyun_config(name, default=None):
    '''
    Get configuration variable from environment variable or
    or django settings.py
    '''
    config = os.environ.get(name, getattr(settings, name, default))
    if config is not None:
        if isinstance(config, str):
            return config.strip()
        else:
            return config
    else:
        raise ImproperlyConfigured(
            'Can not get config for {} either in environment'
            'variable or in settings.py'.format(name))


ACCESS_KEY_ID = get_aliyun_config('ALIYUN_OSS_KEY_ID')
ACCESS_KEY_SCRET = get_aliyun_config('ALIYUN_OSS_KEY_SECRET')
ENDPOINT = get_aliyun_config('ALIYUN_OSS_END_POINT')
BUCKET_NAME = get_aliyun_config('ALIYUN_OSS_BUCKET_NAME')
OSS_TIMEOUT = get_aliyun_config('ALIYUN_OSS_TIMEOUT', 30)

#use MEDIA_ROOT as bucket prefix
BUCKET_PREFIX = getattr(settings, 'MEDIA_ROOT')
MEDIA_URL = getattr(settings, 'MEDIA_URL')

@deconstructible
class AliyunOssStorage(Storage):
    ''' aliyun oss storage '''
    def __init__(self, access_key_id=ACCESS_KEY_ID,
                 access_key_secret=ACCESS_KEY_SCRET,
                 endpoint=ENDPOINT,
                 bucket_name=BUCKET_NAME,
                 timeout=OSS_TIMEOUT):

        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.service = oss2.Service(self.auth, endpoint,
                                    connect_timeout=timeout)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def _open(self, name, mode='rb'):
        name = self._clean_name(name)
        remote_file = AliyunOssFile(name, self, mode=mode)
        return remote_file

    def _read(self, name, byte_range=()):
        name = self._clean_name(name)
        if not byte_range:
            resp = self.bucket.get_object(name)
        else:
            resp = self.bucket.get_object(name, byte_range)

        if resp.status and resp.status / 100 != 2:
            raise IOError('OSSStorageError: status={0}, request_id={1}'.format(
                resp.status, resp.request_id))

        data = resp.read()
        etag = resp.etag if resp.etag else ''
        content_range = resp.headers.get('Content-Range', None)
        content_len = resp.content_length

        return data, etag, content_range, content_len

    def _clean_name(self, name):
        '''help function, useful for windows' path'''
        return os.path.join(BUCKET_PREFIX,
                            os.path.normpath(name).replace('\\', '/'))

    def _save(self, name, content):
        name = self._clean_name(name)
        self.bucket.put_object(name, content)
        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        name = self._clean_name(name)
        self.bucket.delete_object(name)

    def exists(self, name):
        name = self._clean_name(name)
        try:
            r = self.bucket.head_object(name)
            if r.status / 100 == 2:
                return True
            return False
        except Exception as e:
            return False

    def listdir(self):
        pass

    def size(self, name):
        name = self._clean_name(name)
        try:
            r = self.bucket.head_object(name)
            if r.status and r.status / 100 == 2:
                return r.content_length if r.content_length else 0
            return 0
        except Exception as e:
            return 0

    def url(self, name, force=False):
        return '{0}{1}'.format(MEDIA_URL, name)


class AliyunOssFile(File):
    ''' aliyun oss file '''

    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = StringIO()
        self.start_range = 0

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        if num_bytes is None:
            args = ()
            self.start_range = 0
        else:
            args = (self.start_range, self.start_range + num_bytes - 1)
        data, etag, content_range, content_len = self._storage._read(
            self._name, byte_range=args)
        if content_range is not None:
            current_range, size = content_range.split(
                ' ', 1)[1].split('/', 1)  # 'bytes 2-4/10'
            start_range, end_range = current_range.split('-', 1)
            self._size, self.start_range = int(size), int(end_range)+1
        self.file = StringIO(data)
        return self.file.getvalue()

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError('File was opened for read-only access')
        self.file = StringIO(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty:
            self._storage._save(self._name, self.file.getvalue())
        self.file.close()
