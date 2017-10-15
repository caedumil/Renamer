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
import time

from urllib import request as urlRequest
from urllib import error as urlerr
from collections import namedtuple


#
# Class
#
class Web():
    def downloadData(self, mediaTitle, **kwargs):
        saneTitle = (lambda x: re.sub("\W+", "+", x))(mediaTitle)

        if isinstance(self, Movie):
            url = [self.url]
            url.extend(["t={}".format(saneTitle), "y={}".format(kwargs["year"])])
            link = "&".join(url)

        elif isinstance(self, TvShow):
            if kwargs["action"] == "search":
                url = [self.url]
                url.extend(["search", "q={}".format(saneTitle)])
                link = "&".join(url)

            elif kwargs["action"] == "lookup":
                link = self._show.link

        try:
            down = urlRequest.urlopen(link)
            data = down.read()
            text = json.loads(data.decode("UTF-8"))

            if isinstance(text, dict) and text.get("Response") == "False":
                raise NotFoundError("{} - {}".format(text["Error"], mediaTitle))

            return text

        except urlerr.URLError:
            raise DownloadError("Failed to fetch data for {}".format(mediaTitle))


class TvShow(Web):
    def __init__(self, title, country=None, year=None):
        self.url = "http://api.tvmaze.com/search/shows?"
        self._show = None
        self._season = None
        self._curSeason = None

        showInfo = super().downloadData(title, action="search")

        showsList = []
        showCand = namedtuple("Show", ["title", "country", "premier", "link"])
        match = difflib.SequenceMatcher(None, title.upper())
        for entry in [x for x in showInfo if x["show"]["premiered"]]:
            match.set_seq2(entry["show"]["name"].upper())
            if match.quick_ratio() < 0.85:
                continue

            newItem = showCand(title=entry["show"]["name"],
                               country=entry["show"]["network"]["country"]["code"],
                               premier=entry["show"]["premiered"],
                               link="{}/episodes".format(entry["show"]["_links"]["self"]["href"]))
            showsList.append(newItem)

        if not showsList:
            strerror = "Could not find {}.".format(title.upper())
            raise NotFoundError(strerror)

        showsList.sort(key=lambda x: x.premier, reverse=True)

        if year and country:
            selYear = [x for x in showsList
                       if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year]
            selCountry = [x for x in showsList if country == x.country]
            sel = list(filter(lambda x: x in selYear, selCountry))

        elif year:
            sel = [x for x in showsList
                   if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year]

        elif country:
            sel = [x for x in showsList if country == x.country]

        elif len(showsList) > 1:
            tmp = []
            for entry in showsList:
                match.set_seq2(entry.title.upper())
                if match.quick_ratio() == 1:
                    tmp.append(entry)

            sel = tmp

        else:
            sel = showsList

        self._show = sel.pop()

    def populate(self):
        self._epsInfo = super().downloadData(self._show.title, action="lookup")

    @property
    def title(self):
        return self._show.title

    @property
    def season(self):
        return self._curSeason

    @season.setter
    def season(self, season):
        if self._curSeason != season:
            self._curSeason = season
            info = self._epsInfo
            self._season = {"{:0>2}".format(x["number"]): x["name"] for x in info
                            if "{:0>2}".format(x["season"]) == self._curSeason}

    @property
    def seasonEps(self):
        return self._season


class Movie(Web):
    def __init__(self, movieTitle, movieYear):
        self.url = "http://www.omdbapi.com/?r=json"
        self._info = super().downloadData(movieTitle, year=movieYear)

    @property
    def title(self):
        return self._info["Title"]

    @property
    def year(self):
        return self._info["Year"]

    @property
    def IMDB(self):
        return self._info["imdbID"]


#
# Exception
#
class DownloadError(Exception):
    pass


class NotFoundError(Exception):
    pass
