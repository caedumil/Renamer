# Renamer.py

[![Build Status](https://travis-ci.org/caedus75/Renamer.svg?branch=master)](https://travis-ci.org/caedus75/Renamer)

Simple script written in python3 to rename downloaded episodes, based on the
season number, episode number and episode name.

By default it will look online for the information.

- [TV Shows](http://www.tvmaze.com/)


## How to use?

    renamer [-h] [-v] [-y] [-c] FOLDER [FOLDER ...]

* `-h`, `--help` help message
* `-v`, `--version` version information
* `-y`, `--no-confirm` don't ask for confirmation to rename the files
* `-s`, `--simple` create filename without the show name
* `-r`, `--recursive` list content of folders recursively
* `-l`, `--loglevel` Set log level (INFO, WARN, ERROR)
* episodes FOLDER
