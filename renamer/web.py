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
    def __init__(self):
        self.url = [ "http://www.omdbapi.com/?r=json" ]


    def downloadData(self, mediaTitle, **kwargs):
        saneTitle = (lambda x: re.sub("\W+", "+", x))(mediaTitle)
        self.url.append("t={}".format(saneTitle))

        if self.type == "movie":
            self.url.append("y={}".format(kwargs["year"]))

        elif self.type == "series":
            self.url.append("season={}".format(kwargs["season"]))

        try:
            link = "&".join(self.url)
            down = url.urlopen(link)
            data = down.read()
            text =  json.loads(data.decode("UTF-8"))

            if text["Response"] == "False":
                raise NotFoundError("{} - {}".format(text["Error"], mediaTitle))

            return text

        except urlerr.URLError:
            raise DownloadError("Failed to fetch - {}".format(link))


class TvShow(Web):
    def __init__(self, showTitle, showSeason):
        self.type = "series"
        super().__init__()
        self._showInfo = super().downloadData(showTitle, season=showSeason)
        self._episodesTitle = None

        match = difflib.SequenceMatcher(None,
                                        showTitle.upper(),
                                        self._showInfo["Title"].upper())

        if match.ratio() < 0.8:
            strerror = "Searched for {}. Found {}".format(showTitle.upper(),
                                                          self._showInfo["Title"].upper())
            raise NotFoundError(strerror)


    @property
    def showTitle(self):
        return self._showInfo["Title"]


    @property
    def showSeason(self):
        return "{:0>2}".format(self._showInfo["Season"])


    @property
    def episodeTitle(self):
        if not self._episodesTitle:
            self._episodesTitle = { "{:0>2}".format(x["Episode"]): x["Title"]
                                    for x in self._showInfo["Episodes"] }
        return self._episodesTitle


class Movie(Web):
    def __init__(self, movieTitle, movieYear):
        self.type = "movie"
        super().__init__()
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
