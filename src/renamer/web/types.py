# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


#
# Import
#
import re
import json
import time

from collections import namedtuple
from urllib import error as urlerr
from urllib import request as urlRequest

from fuzzywuzzy import process

from . import error


#
# Class
#
class Web():
    def _downloadData(self, link):
        try:
            down = urlRequest.urlopen(link)

        except urlerr.URLError:
            raise error.DownloadError("Failed to fetch data.")

        else:
            data = down.read()
            text = json.loads(data.decode("UTF-8"))
            return text

    def searchShow(self, title):
        saneTitle = re.sub("\W", "+", title)
        url = [self.url]
        url.extend(["search", "q={}".format(saneTitle)])
        link = "&".join(url)
        return self._downloadData(link)

    def lookupShow(self):
        link = self._show.link
        return self._downloadData(link)


class TvShow(Web):
    def __init__(self, title, country=None, year=None):
        self.url = "http://api.tvmaze.com/search/shows?"
        self._show = None
        self._season = None
        self._curSeason = None
        self._show = self._selectShow(self._findShow(title), country, year)

    def _findShow(self, title):
        showCand = namedtuple("Show", ["title", "country", "premier", "thetvdb", "link"])
        showsList = []

        showInfo = self.searchShow(title)
        for entry in [x for x in showInfo if x["show"]["premiered"]]:
            network = entry["show"]["network"]
            webchannel = entry["show"]["webChannel"]
            showProvider = network if network else webchannel
            countryCode = showProvider["country"]["code"] if showProvider["country"] else None

            newItem = showCand(
                title=entry["show"]["name"],
                country=countryCode,
                premier=entry["show"]["premiered"],
                thetvdb=entry["show"]["externals"]["thetvdb"],
                link="{}/episodes".format(entry["show"]["_links"]["self"]["href"])
            )
            showsList.append(newItem)

        candidates = {x: x.title for x in showsList}
        if len(candidates) == 0:
            strerror = "Could not find {}.".format(title.upper())
            raise error.NotFoundError(strerror)

        return [x[2] for x in process.extractBests(title, candidates, score_cutoff=75)]

    def _selectShow(self, showsList, country, year):
        showsList.sort(key=lambda x: x.premier, reverse=True)
        if year and country:
            selYear = [
                x for x in showsList if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year
            ]
            selCountry = [x for x in showsList if country == x.country]
            sel = list(filter(lambda x: x in selYear, selCountry))

        elif year:
            sel = [
                x for x in showsList if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year
            ]

        elif country:
            sel = [x for x in showsList if country == x.country]

        else:
            sel = showsList

        return sel.pop()

    def populate(self):
        self._epsInfo = self.lookupShow()

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
            self._season = {
                "{:0>2}".format(x["number"]): x["name"]
                for x in self._epsInfo if "{:0>2}".format(x["season"]) == self._curSeason
            }

    @property
    def seasonEps(self):
        return self._season

    @property
    def thetvdb(self):
        return self._show.thetvdb
