# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import os
import logging
import platform


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
