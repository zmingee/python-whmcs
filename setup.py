#!/usr/bin/env python3

import re
from setuptools import setup

VERSION = None


def main():
    return setup(version=VERSION)


if __name__ == '__main__':
    with open('pywhmcs/__init__.py') as fp:
        _locals = {}
        exec(fp.read(), None, _locals)
        VERSION = _locals['__version__']

    main()
