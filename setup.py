#
# A setuptools based setup module.
#


import os

from setuptools import setup, find_packages


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    return open(path).read()


setup(
    name="renamer",
    version="0.2.3-dev",

    description="A utility to rename TV files.",
    long_description=_read("README.md"),
    url="https://github.com/caedus75/Renamer",

    author="Carlos Millett",
    author_email="carlos4735@gmail.com",

    license="BSD",

    packages=find_packages("src"),

    package_dir={"": "src"},

    entry_points={
        "console_scripts": [
            "renamer = renamer.ui.cli:main",
        ],
    },

    keywords="utility rename tv show",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",

        "License :: OSI Approved :: BSD License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    python_requires=">=3.4"
)
