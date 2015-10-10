#   Copyright (c) 2015, Carlos Millett
#   All rights reserved.

import os
import re
import shutil

#
# Class
#
class Folder():
    '''
    File information.

    Parse the filename to get:
        - show name
        - season number
        - episode number

    If fails to find, value is set to None.
    '''
    def __init__(self, filename):
        self.path = os.path.dirname(filename)
        self.filename = os.path.basename(filename)
        self._parseName()

    def _formatName(self, show):
        dots = re.compile("[^a-z0-9]", re.I)
        numbers = re.compile("[12][0-9]{3}")

        return numbers.sub("", dots.sub("+", show)).strip("+")

    def _parseName(self):
        regex = re.compile("s(\d{2})e(\d{2})", re.I)
        show = season = episode = None

        splitName = regex.split(self.filename)

        if len(splitName) >= 3:
            show, season, episode = splitName[:3]

        if show:
            self.show = self._formatName(show)
            self.properShow = self.show.replace("+", " ")

        else:
            self.show = None
            self.properShow = None

        self.season = season
        self.episode = episode

    def setEpName(self, name, showName=True):
        '''
        Use name to set the new filename.
        '''
        _, ext = os.path.splitext(self.filename)
        proper = name.replace("/", "-")

        self.epname = \
            "{0} - {1}x{2} - {3}{4}".format(
                self.properShow, self.season, self.episode, proper, ext
            ) \
            if showName else \
            "{0}x{1} - {3}{4}".format(
                self.season, self.episode, proper, ext
            )

    def addShowName(self):
        self.epname = "{0} - {1}".format(self.show, self.epname)

    def rename(self):
        '''
        Rename the file on disk.
        '''
        fname = os.path.join(self.path, self.filename)
        ename = os.path.join(self.path, self.epname)

        shutil.move(fname, ename)
