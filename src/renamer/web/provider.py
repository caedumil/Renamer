# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


#
# Import
#
import re
import json

from urllib import error as urlerr
from urllib import request as urlRequest


#
# Class
#
class Provider():
    def _downloadData(self, link):
        try:
            down = urlRequest.urlopen(link)

        except urlerr.URLError:
            raise error.DownloadError("Failed to fetch data.")

        else:
            data = down.read()
            text = json.loads(data.decode('UTF-8'))
            return text

    def searchShow(self, title):
        saneTitle = re.sub(r'\W', '+', title)
        url = [self.url]
        url.extend(['search', 'q={}'.format(saneTitle)])
        link = '&'.join(url)
        return self._downloadData(link)

    def lookupShow(self, link):
        return self._downloadData(link)


class TVMaze(Provider):
    def __init__(self):
        self.url = 'http://api.tvmaze.com/search/shows?'