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
import argparse

from . import web
from . import localpath
from . import __version__


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
    parser.add_argument("path",
                        type=str,
                        metavar="FILE",
                        nargs="+",
                        help="FILE location.")
    args = parser.parse_args()


    print("Listing files.")
    filesList = []
    for path in [ os.path.abspath(x) for x in args.path if os.path.exists(x) ]:
        if args.recursive and os.path.isdir(path):
            tree = [ (x, y) for x, _, y in os.walk(path) if y ]
            for root, files in tree:
                tmp = map((lambda x: os.path.join(root, x)), files)

        elif os.path.isdir(path):
            tmp = map((lambda x: os.path.join(path, x)), os.listdir(path))

        else:
            tmp = [ path ]

        filesList.extend(tmp)

    if not filesList:
        print("Nothing found.")
        sys.exit()



    print("Reading filename for SERIES information.")
    showFiles = []
    for entry in filesList:
        try:
            fileObj = localpath.SerieFile(entry)
            showFiles.append(fileObj)

        except localpath.MatchNotFoundError as err:
            print(err)


    if not showFiles:
        print("Nothing to do.")
        sys.exit()


    showEps = {}
    for show in set( x.show for x in showFiles ):
        print("Downloading episode names for {0}.".format(show.upper()))
        showEps[show] = web.TvShow(show)


    print("Setting new filename.")
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
            print(err)

        except PermissionError as err:
            print("{0}\n{1}\n".format(err.strerror, err.filename))
            sys.exit(err.errno)


if __name__ == "__main__":
    main()
