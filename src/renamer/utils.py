# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import os
import logging
import platform
from itertools import zip_longest
from pathlib import Path

from .localpath import error as l_error


def setupLogger(loglevel):
    logger = logging.getLogger('Renamer')
    logLevel = getattr(logging, loglevel.upper(), None)
    logger.setLevel(logLevel)

    consoleOut = logging.StreamHandler()
    consoleFormat = logging.Formatter('%(levelname)s - %(message)s')
    consoleOut.setLevel(logging.INFO)
    consoleOut.setFormatter(consoleFormat)

    logDir = os.path.expandvars('%TMP%') if platform.system() == 'Windows' else '/tmp'
    logPath = os.path.join(logDir, 'renamer.log')
    fileOut = logging.FileHandler(logPath, mode='w')
    fileFormat = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
    fileOut.setLevel(logging.WARN)
    fileOut.setFormatter(fileFormat)

    logger.addHandler(consoleOut)
    logger.addHandler(fileOut)
    return logger


def genFilesList(target, recursive=False):
    logger = logging.getLogger('Renamer.Path')
    filesList = []
    for path in [os.path.abspath(x) for x in target if os.path.exists(x)]:
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

    return [Path(x) for x in filesList]


def genShowList(filesList):
    logger = logging.getLogger('Renamer.Path')
    showFiles = []
    for entry in [x for x in filesList if not x.is_dir()]:
        try:
            logger.info('Trying to match patterns to {0}.'.format(entry.name))
            info = match(entry.name)

        except error.MatchNotFoundError as err:
            logger.warn(err)

        else:
            title = names.parse(info.title)
            showFiles.append({'show': title, 'info': info})

    if not showFiles:
        raise error.MatchNotFoundError("No valid filename(s) found.")

    return showFiles
