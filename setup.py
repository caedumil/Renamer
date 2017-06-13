#/usr/bin/env python3

#
# A setuptools based setup module.
#


from setuptools import setup

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
        "Development Status :: 4 - Beta",

        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",

        "License :: OSI Approved :: BSD License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    python_requires = ">=3.4"
)
