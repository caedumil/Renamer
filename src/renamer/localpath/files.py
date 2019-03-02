# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import os
from itertools import zip_longest
from pathlib import Path

from . import error
from .log import logger


def genFilesList(target, recursive=False):
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
