# Django Aliyun Storage

### Django storage for Aliyun Oss

## Install

    For now only support python3. Please install with 
    `python setup.py install`
    or
    `python setup.py bdist_wheel && pip install dist/django_aliyun_storage-0.0.1-py3-none-any.whl`
    or
    `python setup.py sdist && pip install dist/django-aliyun-storage-0.0.1.tar.gz`



## Configurations

    setup these veriable in your environment variable or in settings.py

    ACCESS_KEY_ID, ACCESS_KEY_SCRET  # your aliyun access key id & scret
    ENDPOINT  # your aliyun oss endpoint
    BUCKET_NAME  # your bucket name
    OSS_TIMEOUT  # oss access timeout, default as 30s.
    
    the storage will use your MEIDA_ROOT variable as you bucket file prefix, if you do *not* like this please leave MEDIA_ROOT to ''

## Usage

    in settings.py set "EFAULT_FILE_STORAGE` :

    DEFAULT_FILE_STORAGE = 'aliyunstorage.backends.AliyunOssStorage'

## Changelog

## License
    MIT
