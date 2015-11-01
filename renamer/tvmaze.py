#   Copyright (c) 2015, Carlos Millett
#   All rights reserved.

import re
import json
import urllib.request as url

#
# Class
#
class Show():
    '''
    Query TVMaze.com and download the full episode list for the show
    '''
    def __init__(self, showName):
        self.showName = None
        self.showID = None
        self.showTVDB = None
        self._getID(showName)
        self._getEpJson()

    def _getInfo(self, link):
        down = url.urlopen(link)
        data = down.read()

        return json.loads(data.decode("UTF-8"))

    def _getID(self, show):
        link = "http://api.tvmaze.com/singlesearch/shows?q={}".format(show)
        jason = self._getInfo(link)

        self.showName = jason["name"]
        self.showID = jason["id"]
        self.showTVDB = jason["externals"]["thetvdb"]

        return

    def _getEpJson(self):
        link = "http://api.tvmaze.com/shows/{}/episodes".format(self.showID)
        jason = self._getInfo(link)

        self._showEPs = {
            x:{
                "{:0>2}".format(y["number"]):y["name"]
                for y in jason if "{:0>2}".format(y["season"]) == x
            }
            for x in set( "{:0>2}".format(z["season"]) for z in jason )
        }

        return

    def getSeason(self, season):
        '''
        Return the episode list of season
        '''
        return self._showEPs[season]

    def getTitle(self, season, episode):
        '''
        Return the episode name for season, episode
        '''
        ss = self.getSeason(season)

        names = [ ss[x] for x in episode ]

        return "-".join(names)
