# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
import logging
import platform

from renamer import cli
from renamer import web
from renamer import localpath


def setupLogger(loglevel):
    consoleOut = logging.StreamHandler()
    consoleFormat = logging.Formatter("%(levelname)s - %(message)s")
    consoleOut.setLevel(logging.INFO)
    consoleOut.setFormatter(consoleFormat)

    logDir = os.path.expandvars("%TMP%") if platform.system() == "Windows" else "/tmp"
    logPath = os.path.join(logDir, "renamer.log")
    logLevel = getattr(logging, loglevel.upper(), None)
    fileOut = logging.FileHandler(logPath, mode="w")
    fileFormat = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
    fileOut.setLevel(logging.WARN)
    fileOut.setFormatter(fileFormat)

    logger = logging.getLogger("Renamer")
    logger.setLevel(logLevel)
    logger.addHandler(consoleOut)
    logger.addHandler(fileOut)

    return logger


def buildNewFileNames(showFiles, showInfo, short=False):
    for ep in showFiles:
        serie = showInfo[ep.identifier].title
        showInfo[ep.identifier].season = ep.season
        episode = "-".join(ep.episodes)
        title = "-".join([showInfo[ep.identifier].seasonEps[x] for x in ep.episodes])
        newFileName = "{1}x{2} - {3}" if short else "{0} - {1}x{2} - {3}"
        ep.newFileName = newFileName.format(serie, ep.season, episode, title)


def askApplyChanges(no_confirmation):
    if not no_confirmation:
        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            return False
    return True


def main():
    parser = cli.setParser()
    args = parser.parse_args()
    logger = setupLogger(args.loglevel)

    try:
        showFiles = localpath.genFilesList(args.path, args.recursive)
        showInfo = web.genShowsDict(showFiles)

    except FileNotFoundError as err:
        return 1

    except localpath.error.MatchNotFoundError:
        return 1

    except web.error.NotFoundError as err:
        return 1

    else:
        web.populateShows(showInfo)

    logger.info("Setting new filename(s).")
    buildNewFileNames(showFiles, showInfo, args.simple)
    showFiles.sort(key=lambda x: x.newFileName)
    printableList = [
        "--- {0}\n+++ {1}".format(i.curFileName, i.newFileName)
        for i in showFiles
    ]
    print("\n".join(printableList))

    if not askApplyChanges(args.no_confirm):
        return 0

    for ep in showFiles:
        try:
            ep.rename()

        except localpath.error.SameFileError as err:
            logger.warn(err)

        except PermissionError as err:
            strerr = "Can't rename {0} - {1}.".format(ep.curFileName, err.strerror)
            logger.error(strerr)

    return 0


if __name__ == "__main__":
    main()
