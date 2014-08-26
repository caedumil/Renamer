# Renamer.py

Simple script written in python3 to rename downloaded episodes, based on the
season number, episode number and episode name.

## How to use?

    renamer.py [-h] -s SEASON -p PATH -f FILE

* `-h` help message
* `-s` number of the season
* `-p` folder path
* `-f` file with episodes names

The episode file is a CSV-style file with one episode per line, like this:

    [episode number]; [episode name]
