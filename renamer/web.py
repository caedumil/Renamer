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
import re
import json
import difflib

from urllib import request as url
from urllib import error as urlerr


#
# Class
#
class Web():
    def downloadData(self, mediaTitle, **kwargs):
        saneTitle = (lambda x: re.sub("\W+", "+", x))(mediaTitle)

        if self.type == "movie":
            self.url.extend([ "t={}".format(saneTitle), "y={}".format(kwargs["year"]) ])

        elif self.type == "tvshow":
            self.url.extend([ "q={}".format(saneTitle) , "embed=episodes" ])

        try:
            link = "&".join(self.url)
            down = url.urlopen(link)
            data = down.read()
            text =  json.loads(data.decode("UTF-8"))

            if text.get("Response") == "False":
                raise NotFoundError("{} - {}".format(text["Error"], mediaTitle))

            return text

        except urlerr.URLError:
            raise DownloadError("Failed to fetch - {}".format(link))


class TvShow(Web):
    def __init__(self, showTitle):
        self.type = "tvshow"
        self.url = [ "http://api.tvmaze.com/singlesearch/shows?" ]
        self._showInfo = super().downloadData(showTitle)
        self._season = None
        self._curSeason = None

        match = difflib.SequenceMatcher(None,
                                        showTitle.upper(),
                                        self._showInfo["name"].upper())

        if match.ratio() < 0.8:
            strerror = "Searched for {}. Found {}".format(showTitle.upper(),
                                                          self._showInfo["name"].upper())
            raise NotFoundError(strerror)


    @property
    def showTitle(self):
        return self._showInfo["name"]


    @property
    def showSeason(self):
        return self._season


    @showSeason.setter
    def showSeason(self, season):
        if self._curSeason != season:
            self._curSeason = season
            _info = self._showInfo["_embedded"]["episodes"]
            self._season = { "{:0>2}".format(x["number"]):x["name"] for x in _info
                             if "{:0>2}".format(x["season"]) == self._curSeason
                           }


class Movie(Web):
    def __init__(self, movieTitle, movieYear):
        self.type = "movie"
        self.url = [ "http://www.omdbapi.com/?r=json" ]
        self._info = super().downloadData(movieTitle, year=movieYear)


    @property
    def movieTitle(self):
        return self._info["Title"]


    @property
    def movieYear(self):
        return self._info["Year"]


    @property
    def movieIMDB(self):
        return self._info["imdbID"]


#
# Exception
#
class DownloadError(Exception):
    pass


class NotFoundError(Exception):
    pass
