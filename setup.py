"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import renamer

setup(
    name='renamer',

    version = renamer.__version__,

    description = 'A utility to rename downloaded tv shows',

    long_description = renamer.__doc__,

    url='https://github.com/caedus75/Renamer',

    author = renamer.__author__,

    author_email = renamer.__email__,

    license = 'BSD',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop'
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='utility rename tv show',

    packages=['renamer'],

    entry_points={
        'console_scripts': [
            'renamer = renamer.__main__:main',
        ],
    },
)
