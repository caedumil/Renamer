#/usr/bin/env python3

# A setuptools based setup module.
#
# See:
# https://packaging.python.org/en/latest/distributing.html
# https://github.com/pypa/sampleproject


from setuptools import setup, find_packages
from codecs import open
from os import path

import renamer


setup(
    name = "renamer",
    version = renamer.__version__,
    description = "A utility to rename TV files.",
    long_description = renamer.__doc__,
    url = "https://github.com/caedus75/Renamer",
    author = renamer.__author__,
    author_email = renamer.__email__,
    license = "BSD",

    packages = [
        "renamer",
        "renamer.ui"
    ],

    entry_points = {
        "console_scripts": [
            "renamer = renamer.ui.cli:main",
        ],
    },

    keywords = "utility rename tv show",

    classifiers = [
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",

        # Indicate who your project is intended for
        "Intended Audience :: End Users/Desktop"
        "Topic :: Utilities",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: BSD License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
