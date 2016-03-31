from setuptools import setup, find_packages

import io
import os

if os.environ.get('USER','') == 'vagrant':
    del os.link

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
try:
    with io.open('DESCRIPTION.rst', encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    # When travis install the package from the github clone,
    # it cant's find DESCRIPTION.rst
    long_description = ""

setup(
    name="django-aliyun-storage",
    version="0.0.0",
    description="Django storage for Aliyun OSS Storage",
    long_description=long_description,

    # The project URL.
    url='https://github.com/tiany/django-aliyun-storage',

    # Author details
    author='Tiany Wang',
    author_email='lonelinsky@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Plugins',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='aliyun oss django',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["contrib", "docs", "tests*","demo-project"]),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = ['oss2>=2.0.6'],
)
