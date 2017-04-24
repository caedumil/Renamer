# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#
# Import
#
import os
import re

from shutil import move
from itertools import zip_longest


#
# Class
#
class LocalPath():
    def __init__(self, filename):
        self.dirName = os.path.dirname(filename)
        self.curFileName = os.path.basename(filename)
        self.fileNameExt = os.path.splitext(filename)[-1]
        self._newFileName = None


    def rename(self):
        cur = os.path.join(self.dirName, self.curFileName)
        new = os.path.join(self.dirName, self._newFileName)

        if cur == new:
            raise SameFileError("{} and {} are the same file.".format(cur, new))

        move(cur, new)


    @property
    def newFileName(self):
         return self._newFileName


    @newFileName.setter
    def newFileName(self, newName):
        new = self._sanitizeName(newName)
        self._newFileName = "{}{}".format(new, self.fileNameExt)


    def _sanitizeName(self, name):
        table = {
                 ord("á"): "a",
                 ord("à"): "a",
                 ord("ã"): "a",
                 ord("â"): "a",
                 ord("é"): "e",
                 ord("è"): "e",
                 ord("ẽ"): "e",
                 ord("ê"): "e",
                 ord("í"): "i",
                 ord("ì"): "i",
                 ord("ĩ"): "i",
                 ord("î"): "i",
                 ord("ó"): "o",
                 ord("ò"): "o",
                 ord("õ"): "o",
                 ord("ô"): "o",
                 ord("ú"): "u",
                 ord("ù"): "u",
                 ord("ũ"): "u",
                 ord("û"): "u",
                 ord("ç"): "c",
                 ord("ñ"): "n",
                 ord(":"): " -",
                 ord(">"): None,
                 ord("<"): None,
                 ord("?"): None,
                 ord("!"): None,
                 ord("*"): None,
                 ord("#"): None,
                 ord("/"): None,
                 ord("\\"): None,
                 ord("\""): None,
                 ord("\'"): None
                }

        return name.translate(table)


    def _formatName(self, name):
        sep = re.compile("[\W]+")
        year = re.compile("[12][0-9]{3}")
        country = re.compile("[A-Z]{2}")

        formated = year.sub("", country.sub("", name))
        formated = sep.sub(" ", formated).strip()

        return formated.title()


class SerieFile(LocalPath):
    def __init__(self, filename):
        super().__init__(filename)
        regex1 = re.compile("\.S(\d{2})((E\d{2})+)\.")
        regex2 = re.compile("\.(\d{4}.)?(\d{3,})\.")

        if regex1.search(self.curFileName):
            show, season, info = regex1.split(self.curFileName)[:3]
            eps = re.findall("\d{2}", info)

        elif regex2.search(self.curFileName):
            show, _, info = regex2.split(self.curFileName)[:3]

            info_lst = list(info)
            info_lst.reverse()
            info_itr = [ iter(info_lst) ] * 2
            info_grp = zip_longest(*info_itr, fillvalue="0")
            info_lst = list(info_grp)
            s_num, s_dec = info_lst.pop()
            info_lst.reverse()

            season = "{}{}".format(s_dec, s_num)
            eps = [ "{}{}".format(e_dec, e_num) for e_num, e_dec in info_lst ]

        else:
            strerror = "Can't find show pattern for {}".format(self.curFileName)
            raise MatchNotFoundError(strerror)

        self.show = super()._formatName(show)
        self.season = "{:0>2}".format(season)
        self.episodes = eps


class MovieFile(LocalPath):
    def __init__(self, filename):
        super().__init__(filename)
        regex = re.compile("([a-z0-9.-]+).([12][0-9]{3})", re.I)

        if not regex.search(self.curFileName):
            strerror = "Can't find movie pattern for {}".format(self.curFileName)
            raise MatchNotFoundError(strerror)

        splitName = regex.findall(self.curFileName)
        movie, year = splitName[0]

        self.title = super()._formatName(movie)
        self.year = year


#
# Exception
#
class MatchNotFoundError(Exception):
    pass

class SameFileError(Exception):
    pass
