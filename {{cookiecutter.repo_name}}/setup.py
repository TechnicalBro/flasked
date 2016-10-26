#!/usr/bin/env python3
import codecs
import os
import re
from setuptools import setup, find_packages
from pip.req import parse_requirements

INSTALL_REQS = parse_requirements(
    'requirements.txt',
    session=False
)
REQS = [str(ir.req) for ir in INSTALL_REQS]

NAME = '{{cookiecutter.app_name}}'
VERSION = '{{cookiecutter.version}}'

PACKAGES = find_packages(exclude=['tests*', 'logs*', 'docs*'])

# META_PATH = os.path.join("src", "attr", "__init__.py")

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


# META_FILE = read(META_PATH)
META_FILE = None


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def main():
    setup(
        name=NAME,
        version=VERSION,
        description='{{cookiecutter.short_description}}',
        license='MIT',
        long_description='',
        author='{{cookiecutter.full_name}}',
        author_email='{{cookiecutter.email}}',
        url='',
        packages=PACKAGES,
        include_package_data=True,
        install_requires=REQS,
        entry_points={

        },
        package_data={
            'static': '{{cookiecutter.app_name}}/static/*',
            'templates': '{{cookiecutter.app_name}}/templates/*'
        },
        zip_safe=False,
    )


if __name__ == '__main__':
    main()
