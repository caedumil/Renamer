# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import logging
from pathlib import Path
from typing import List

from .errors import EmptyListError
from .filename import (
    Media,
    Animes,
    Series,
    Movies
)


def setupLogger(loglevel: str) -> logging.Logger:
    logger = logging.getLogger('Renamer')
    logLevel = getattr(logging, loglevel, None)
    logger.setLevel(logLevel)

    consoleOut = logging.StreamHandler()
    consoleFormat = logging.Formatter('%(levelname)s - %(message)s')
    consoleOut.setLevel(logLevel)
    consoleOut.setFormatter(consoleFormat)

    logDir = Path('/tmp')
    logPath = logDir / 'renamer.log'
    fileOut = logging.FileHandler(logPath, mode='w')
    fileFormat = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
    fileOut.setLevel(logging.WARN)
    fileOut.setFormatter(fileFormat)

    logger.addHandler(consoleOut)
    logger.addHandler(fileOut)
    return logger


def genFilesList(target: List[Path]) -> List[Path]:
    filesList: List[Path]
    tmp: List[Path]

    logger = logging.getLogger('Renamer.path')
    filesList = []
    for path in [x.resolve() for x in target if x.exists()]:
        if path.is_dir():
            logger.info("Listing {0}.".format(path))
            tmp = [x.resolve() for x in path.iterdir()]
        else:
            logger.info("Including {0}.".format(path))
            tmp = [path]
        filesList.extend(tmp)

    if not filesList:
        raise EmptyListError("File(s) not found:", target)

    return filesList


def matchFiles(filesList: List[Path]) -> List[Media]:
    parsedList: List[Media]
    tmp: Media

    logger = logging.getLogger('Renamer.filename')
    parsedList = []
    for path in filesList:
        if Animes.match(path.name):
            logger.info("Anime: {0}.".format(path.name))
            tmp = Animes(path)
        elif Series.match(path.name):
            logger.info("Serie: {0}.".format(path.name))
            tmp = Series(path)
        elif Movies.match(path.name):
            logger.info("Movie: {0}.".format(path.name))
            tmp = Movies(path)
        else:
            logger.warning("No match for {0}.".format(path.name))
            continue
        parsedList.append(tmp)

    if not parsedList:
        raise EmptyListError("Could not match file(s) to any media type:", filesList)

    return parsedList


def processFiles(filesList: List[Media]) -> None:
    logger = logging.getLogger('Renamer.rename')
    for media in filesList:
        newFile = media.path.with_name(media.title)
        logger.info("\tOLD: {0}.\n\tNEW: {1}.".format(media.path.name, newFile.name))
        media.path.rename(newFile)
