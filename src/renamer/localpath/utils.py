# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.

#
# Import
#
import os
import logging

from . import types, error


#
# Global var
#
logger = logging.getLogger('Renamer.Files')


#
# Function
#
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
