# Renamer.py

Simple script written in python3 to rename downloaded episodes, based on the
season number, episode number and episode name.

By default it will look online for the information.


## How to use?

    renamer.py [-h] [-v] [-y] [-c] FOLDER [FOLDER ...]

* `-h`, `--help` help message
* `-v`, `--version` version information
* `-y`, `--no-confirm` don't ask for confirmation to rename the files
* `-c`, `--complete` add show nome to the filename
* episodes FOLDER

The FILE is a plain text file with one episode name per line.
