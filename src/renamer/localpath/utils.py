# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import os
import re
import logging
from itertools import zip_longest

from . import types, error


logger = logging.getLogger('Renamer.Files')


def traversePath(path, recursive):
    filesList = []
    for path in [os.path.abspath(x) for x in path if os.path.exists(x)]:
        if recursive and os.path.isdir(path):
            logger.info('Descending into {0}.'.format(path))
            tmp = []
            tree = [(x, y) for x, _, y in os.walk(path) if y]
            for root, files in tree:
                tmp.extend(map((lambda x: os.path.join(root, x)), files))

        elif os.path.isdir(path):
            logger.info('Entering {0}.'.format(path))
            tmp = map((lambda x: os.path.join(path, x)), os.listdir(path))

        else:
            logger.info('Listing {0}.'.format(path))
            tmp = [path]

        filesList.extend(tmp)

    if not filesList:
        raise FileNotFoundError("File(s) not found.")

    return filesList


def genFilesList(path, recursive=False):
    filesList = traversePath(path, recursive)

    showFiles = []
    for entry in [x for x in filesList if not os.path.isdir(x)]:
        try:
            logger.info('Trying to match patterns to {0}.'.format(os.path.basename(entry)))
            fileObj = types.SerieFile(entry)

        except error.MatchNotFoundError as err:
            logger.warn(err)

        else:
            showFiles.append(fileObj)

    if not showFiles:
        raise error.MatchNotFoundError("No valid filename(s) found.")

    return showFiles


def matchShow(fileName):
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

    return (show, season, eps)
