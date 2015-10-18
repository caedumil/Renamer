#!/usr/bin/env  python3

#   Copyright (c) 2015, Carlos Millett
#   All rights reserved.

import os
import sys
import argparse
import urllib.error as urlerr

import tvmaze as tv
import folder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s -- 0.0.1.dev1"
    )
    parser.add_argument(
        "-y", "--no-confirm", action="store_true",
        help="Do not ask for confirmation"
    )
    parser.add_argument(
        "-c", "--complete", action="store_true",
        help="Add the serie name to the final filename"
    )
    parser.add_argument(
        "path", type=str, metavar="FILE", nargs="+",
        help="FILE location"
    )
    args = parser.parse_args()

    fileList = []
    for path in [ x for x in args.path if os.path.exists(x) ]:
        if os.path.isdir(path):
            content = map((lambda x: os.path.join(path, x)), os.listdir(path))

        else:
            content = [ os.path.join(os.curdir, path) ]

        fileList += [ x for x in content ]

    files = [ x for x in map((lambda x: folder.Folder(x)), fileList) if x.show ]

    if not files:
        print("Nothing to do...")
        sys.exit(1)

    shows = {}
    for serie, proper in set( (x.show, x.properShow) for x in files ):
        try:
            print("Downloading episode list for {0}.".format(proper))
            shows[serie] = tv.Show(serie)

        except urlerr.URLError as err:
            print("Cant download list for {0}".format(proper))
            print("{0}".format(err.strerror))

    for ep in files:
        ep.properShow = shows[ep.show].showName
        if args.complete:
            ep.setFullName(shows[ep.show].getTitle(ep.season, ep.episode))

        else:
            ep.setEpName(shows[ep.show].getTitle(ep.season, ep.episode))

    files.sort(key=lambda x: x.epname)

    if not args.no_confirm:
        for ep in files:
            print("<<< {0}\n>>> {1}".format(ep.filename, ep.epname))

        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            sys.exit(1)

    try:
        for ep in files:
            ep.rename()

    except PermissionError as err:
        print("{0}\n{1}".format(err.strerror, err.filename))
        sys.exit(err.errno)

if __name__ == "__main__":
    main()
