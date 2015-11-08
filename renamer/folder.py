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
        self.show = None
        self.properShow = None
        self.season = None
        self.episode = None
        self._parseName()

    def _formatName(self, show):
        dots = re.compile("[^a-z0-9]", re.I)
        numbers = re.compile("[12][0-9]{3}")

        name = numbers.sub("", dots.sub("+", show)).strip("+")

        return name.upper()

    def _episode(self, ep):
        regex = re.compile("(\d{2})")

        return regex.findall(ep)

    def _parseName(self):
        regex1 = re.compile("s?(\d{1,2})[ex](\d{2}(\.?[ex-]\d{2})*)", re.I)
        regex2 = re.compile("(\d{2})(\d{2,)")
        regex3 = re.compile("(\d)(\d{2,})")

        if regex1.search(self.filename):
            regex = regex1

        elif regex2.search(self.filename):
            regex = regex2

        elif regex3.search(self.filename):
            regex = regex3

        else:
            return

        splitName = regex.split(self.filename)
        show, season, episode = splitName[:3]

        self.show = self._formatName(show)
        self.properShow = self.show.replace("+", " ")
        self.season = "{:0>2}".format(season)
        self.episode = self._episode(episode)

        return

    def setEpName(self, name):
        '''
        Use name to set the new filename.
        '''
        _, ext = os.path.splitext(self.filename)
        properName = name.replace("/", "-")
        properEp = "-".join(self.episode)

        self.epname = \
            "{0}x{1} - {2}{3}".format(self.season, properEp, properName, ext)

    def setFullName(self, name):
        '''
        Prepend show name to the formated filename
        '''
        self.setEpName(name)
        self.epname = "{0} - {1}".format(self.properShow, self.epname)

    def rename(self):
        '''
        Rename the file on disk.
        '''
        fname = os.path.join(self.path, self.filename)
        ename = os.path.join(self.path, self.epname)

        shutil.move(fname, ename)
