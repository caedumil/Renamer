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
        self.serieSearch ="http://api.tvmaze.com/singlesearch/shows?q={}"
        self.serieEps = "http://api.tvmaze.com/shows/{}/episodes"
        self.movieSearch = "http://www.omdbapi.com/?t={}&y={}&plot=short&r=json"


    def downloadData(self, **kwargs):
        if kwargs.get("title") and kwargs.get("year"):
            saneName = (lambda x: re.sub("\W+", "+", x))(kwargs["title"])
            link = self.movieSearch.format(saneName.upper(), kwargs["year"])

        elif kwargs.get("title"):
            saneName = (lambda x: re.sub("\W+", "+", x))(kwargs["title"])
            link = self.serieSearch.format(saneName.upper())

        elif kwargs.get("id"):
            link = self.serieEps.format(kwargs["id"])

        try:
            down = url.urlopen(link)
            data = down.read()

            return json.loads(data.decode("UTF-8"))

        except urlerr.URLError:
            raise DownloadError("Failed to fetch - {}".format(link))


class TvShow(Web):
    def __init__(self, showTitle):
        super().__init__()
        self._showInfo = super().downloadData(title=showTitle)
        self._episodesIndex = None

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
    def showTVDB(self):
        return self._showInfo["externals"]["thetvdb"]


    @property
    def episodesIndex(self):
        if not self._episodesIndex:
            info = super().downloadData(id=self._showInfo["id"])
            self._episodesIndex = {
                    "{:0>2}".format(x): {
                    "{:0>2}".format(y["number"]): y["name"]
                    for y in info if y["season"] == x
                }
                for x in set( z["season"] for z in info )
            }
        return self._episodesIndex


class Movie(Web):
    def __init__(self, movieTitle, movieYear):
        super().__init__()
        self._info = super().downloadData(title=movieTitle, year=movieYear)

        if not bool(self._info["Response"]):
            title = movieTitle.upper()
            raise NotFoundError("{} - {}".format(self._info["Error"], title))


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
