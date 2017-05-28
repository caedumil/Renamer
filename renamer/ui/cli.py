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
import sys
import logging
import argparse
import platform

from renamer import web
from renamer import localpath
from renamer import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=__version__)
    parser.add_argument("-y",
                        "--no-confirm",
                        action="store_true",
                        help="Do not ask for confirmation.")
    parser.add_argument("-s",
                        "--simple",
                        action="store_true",
                        help="Omit show title from filename.")
    parser.add_argument("-r",
                        "--recursive",
                        action="store_true",
                        help="Recursively descend into directories.")
    parser.add_argument("-l",
                        "--loglevel",
                        metavar="LEVEL",
                        default="INFO",
                        type=str,
                        help="Set log level (INFO, WARN, ERROR).")
    parser.add_argument("path",
                        type=str,
                        metavar="FILE",
                        nargs="+",
                        help="FILE location.")
    args = parser.parse_args()


    logDir = os.path.expandvars("%TMP%") if platform.system() == "Windows" else "/tmp"
    logPath = os.path.join(logDir, "renamer.log")
    logLevel = getattr(logging, args.loglevel.upper(), None)

    consoleOut = logging.StreamHandler()
    consoleFormat = logging.Formatter("%(levelname)s - %(message)s")
    consoleOut.setLevel(logging.INFO)
    consoleOut.setFormatter(consoleFormat)

    fileOut = logging.FileHandler(logPath, mode="w")
    fileFormat = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
    fileOut.setLevel(logging.WARN)
    fileOut.setFormatter(fileFormat)

    logger = logging.getLogger("renamer")
    logger.setLevel(logLevel)
    logger.addHandler(consoleOut)
    logger.addHandler(fileOut)


    filesList = []
    for path in [ os.path.abspath(x) for x in args.path if os.path.exists(x) ]:
        if args.recursive and os.path.isdir(path):
            logger.info("Descending into {0}.".format(path))
            tmp = []
            tree = [ (x, y) for x, _, y in os.walk(path) if y ]
            for root, files in tree:
                tmp.extend(map((lambda x: os.path.join(root, x)), files))

        elif os.path.isdir(path):
            logger.info("Entering {0}.".format(path))
            tmp = map((lambda x: os.path.join(path, x)), os.listdir(path))

        else:
            logger.info("Listing {0}.".format( path))
            tmp = [ path ]

        filesList.extend(tmp)

    if not filesList:
        logger.error("No valid file(s) found.")
        sys.exit()

    filesList =  [ x for x in filesList if not os.path.isdir(x) ]


    showFiles = []
    for entry in filesList:
        try:
            logger.info("Trying to match patterns to {0}.".format(os.path.basename(entry)))
            fileObj = localpath.SerieFile(entry)
            showFiles.append(fileObj)

        except localpath.MatchNotFoundError as err:
            logger.warn(err)


    if not showFiles:
        logger.error("No valid filename(s) found.")
        sys.exit()


    showEps = {}
    for show in set( x.show for x in showFiles ):
        try:
            logger.info("Downloading episode list for {0}.".format(show.upper()))
            showEps[show] = web.TvShow(show)

        except ( web.DownloadError, web.NotFoundError ) as err:
            logger.warn(err)
            showFiles = [ x for x in showFiles if x.show != show ]


    if not showEps:
        logger.error("Could not download list of episodes for any show.")
        sys.exit()


    logger.info("Setting new filename(s).")
    for ep in showFiles:
        serie = showEps[ep.show].showTitle
        showEps[ep.show].showSeason = ep.season
        episode = "-".join(ep.episodes)
        title = "-".join( [ showEps[ep.show].showSeason[x] for x in ep.episodes ] )
        newFileName = "{1}x{2} - {3}" if args.simple else "{0} - {1}x{2} - {3}"

        ep.newFileName = newFileName.format(serie, ep.season, episode, title)


    showFiles.sort(key=lambda x: x.newFileName)
    for i in showFiles:
        print("--- {0}\n+++ {1}".format(i.curFileName, i.newFileName))


    if not args.no_confirm:
        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            sys.exit(1)


    for ep in showFiles:
        try:
            ep.rename()

        except localpath.SameFileError as err:
            logger.warn(err)

        except PermissionError as err:
            strerr = "Can't rename {0} - {1}.".format(ep.curFileName, err.strerror)
            logger.error(strerr)


if __name__ == "__main__":
    main()
