# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
from itertools import zip_longest

from . import names
from . import error
from .log import logger


class Show():
    def __init__(self, title, season, episodes):
        self._title = title
        self._season = '{:0>2}'.format(season)
        self._episodes = ['{:0>2}'.format(x) for x in episodes]

    @property
    def title(self):
        return self._title

    @property
    def season(self):
        return self._season

    @property
    def episodes(self):
        return self._episodes


def match(fileName):
    rSceneRule = re.compile(r'[ .]S(\d{2})((E\d{2}-?)+)[ .]', re.I)
    rPreFormat = re.compile(r' (\d{2})x((\d{2}-?)+) ')
    rAltFormat = re.compile(r'\.(\d{4}.)?(\d{3,})\.')

    if rSceneRule.search(fileName):
        show, season, info = rSceneRule.split(fileName)[:3]
        eps = re.findall(r'\d{2}', info)

    elif rPreFormat.search(fileName):
        show, season, info = rPreFormat.split(fileName)[:3]
        eps = re.findall(r'\d{2}', info)

    elif rAltFormat.search(fileName):
        show_piece, year, info = rAltFormat.split(fileName)[:3]
        show = '{}{}'.format(show_piece, year) if year else show_piece

        info_lst = list(info)
        info_lst.reverse()
        info_itr = [iter(info_lst)] * 2
        info_grp = zip_longest(*info_itr, fillvalue='0')
        info_lst = list(info_grp)
        s_num, s_dec = info_lst.pop()
        info_lst.reverse()

        season = '{}{}'.format(s_dec, s_num)
        eps = ['{}{}'.format(e_dec, e_num) for e_num, e_dec in info_lst]

    else:
        strerror = "Can't find show pattern for {}".format(fileName)
        raise error.MatchNotFoundError(strerror)

    return Show(show, season, eps)


def genShowList(filesList):
    showFiles = []
    for entry in [x for x in filesList if not x.is_dir()]:
        try:
            logger.info('Trying to match patterns to {0}.'.format(entry.name))
            info = match(entry.name)

        except error.MatchNotFoundError as err:
            logger.warn(err)

        else:
            name = names.parse(info.title)
            showFiles.append({'show': name, 'info': info})

    if not showFiles:
        raise error.MatchNotFoundError("No valid filename(s) found.")

    return showFiles
