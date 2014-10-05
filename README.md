# Renamer.py

Simple script written in python3 to rename downloaded episodes, based on the
season number, episode number and episode name.

## How to use?

    renamer.py [-h] -f FILE FOLDER

* `-h` help message
* `-f` file with episodes names
* FOLDER path

The FILE is a plain text file with one episode name per line.  
In the case of a 00 episode, the name must be the last one.
