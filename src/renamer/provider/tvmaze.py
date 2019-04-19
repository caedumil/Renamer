# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
import json
from urllib import error as urlerr
from urllib import request as urlRequest

from . import base
from . import error


TVMaze = base.Provider(url='http://api.tvmaze.com/search/shows?')


def _downloadData(link):
    try:
        down = urlRequest.urlopen(link)

    except urlerr.URLError:
        raise error.DownloadError("Failed to fetch data.")

    else:
        data = down.read()
        text = json.loads(data.decode('UTF-8'))
        return text


def search(title, limit=5):
    saneTitle = re.sub(r'\W', '+', title)
    url = [TVMaze.url, 'search', 'q={}'.format(saneTitle)]
    link = '&'.join(url)
    data = _downloadData(link)
    results = []
    for show in [x['show'] for x in data[:limit] if x['show']['premiered']]:
        network = show['network']
        channel = network if network else show['webChannel']
        countrycode = channel['country']['code'] if channel['country'] else None
        image = show['image']['medium'] if show['image'] else None
        item = base.Show(
            title=show['name'],
            country=countrycode,
            premier=show['premiered'],
            thetvdb=show['externals']['thetvdb'],
            image=image,
            episodes='{}/episodes'.format(show['_links']['self']['href'])
        )
        results.append(item)

    if not results:
        strerror = "Could not find {}".format(title.upper())
        raise error.NotFoundError(strerror)
    return results


def lookup(show):
    data = _downloadData(show.episodes)
    episodes = {}
    for ep in data:
        season = '{:0>2}'.format(ep['season'])
        number = '{:0>2}'.format(ep['number'])
        item = base.Episode(
            name=ep['name'],
            season=season,
            number=number,
            airdate=ep['airdate'],
            image=ep['image']['medium']
        )
        if not episodes.get(season):
            episodes[season] = {}
        episodes[season][number] = item
    return episodes
