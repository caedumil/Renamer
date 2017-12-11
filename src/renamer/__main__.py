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

from renamer import cli
from renamer import web
from renamer import logging
from renamer import localpath


def main():
    parser = cli.setParser()
    args = parser.parse_args()

    logger = logging.setLogger(args.loglevel)

    filesList = []
    for path in [os.path.abspath(x) for x in args.path if os.path.exists(x)]:
        if args.recursive and os.path.isdir(path):
            logger.info("Descending into {0}.".format(path))
            tmp = []
            tree = [(x, y) for x, _, y in os.walk(path) if y]
            for root, files in tree:
                tmp.extend(map((lambda x: os.path.join(root, x)), files))

        elif os.path.isdir(path):
            logger.info("Entering {0}.".format(path))
            tmp = map((lambda x: os.path.join(path, x)), os.listdir(path))

        else:
            logger.info("Listing {0}.".format(path))
            tmp = [path]

        filesList.extend(tmp)

    if not filesList:
        logger.error("No valid file(s) found.")
        sys.exit()

    filesList = [x for x in filesList if not os.path.isdir(x)]

    showFiles = []
    for entry in filesList:
        try:
            logger.info("Trying to match patterns to {0}.".format(os.path.basename(entry)))
            fileObj = localpath.SerieFile(entry)
            showFiles.append(fileObj)

        except localpath.error.MatchNotFoundError as err:
            logger.warn(err)

    if not showFiles:
        logger.error("No valid filename(s) found.")
        sys.exit()

    showEps = {}
    for show in set((x.title, x.country, x.year, x.identifier) for x in showFiles):
        try:
            logger.info("Downloading information for {0}.".format(show[0].upper()))
            showEps[show[3]] = web.TvShow(show[0], show[1], show[2])

        except (web.error.DownloadError, web.error.NotFoundError) as err:
            logger.warn(err)
            showFiles = [x for x in showFiles if x.title != show[0]]

    if showEps:
        for show in showEps.values():
            logger.info("Downloading episodes list for {0}.".format(show.title))
            show.populate()

    else:
        logger.error("Could not download list of episodes for any show.")
        sys.exit()

    logger.info("Setting new filename(s).")
    for ep in showFiles:
        serie = showEps[ep.identifier].title
        showEps[ep.identifier].season = ep.season
        episode = "-".join(ep.episodes)
        title = "-".join([showEps[ep.identifier].seasonEps[x] for x in ep.episodes])
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

        except localpath.error.SameFileError as err:
            logger.warn(err)

        except PermissionError as err:
            strerr = "Can't rename {0} - {1}.".format(ep.curFileName, err.strerror)
            logger.error(strerr)


if __name__ == "__main__":
    main()
