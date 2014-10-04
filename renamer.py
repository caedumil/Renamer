#!/usr/bin/env python3

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
import re
import sys
import argparse
import mimetypes

#
# Classes
#
class LFile():
    '''
    Local Filesystem.
    Holds information of the file on disk.
    '''
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.ext = filename.split(".")[-1]

    def rename(self, ename):
        '''
        Rename file using provided string.
        '''
        self.full_fname = os.path.join(self.path, self.filename)
        self.full_ename = os.path.join(self.path, ename)

        os.rename(self.full_fname, self.full_ename)

class Episode(LFile):
    '''
    Inherits from LFile.
    '''
    def __init__(self, season, enumber, ename, fname, fpath):
        super().__init__(fname, fpath)
        self.season = "%02i"%(int(season))
        self.enumber = "%02i"%(int(enumber))
        self.ename = ename
        self.full_ename = "{0}x{1} - {2}.{3}".format(
            self.season, self.enumber, self.ename, self.ext)

    def rename(self):
        '''
        Extends superclass method to rename the file on disk.
        '''
        super().rename(self.full_ename)

    def __str__(self):
        return ">>> {0}\n<<< {1}".format(self.filename, self.full_ename)

#
# Functions
#
def parse_cli():
    '''
    Set and parse command-line arguments.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("--no-confirm", action="store_true",
        help="Don not ask for confirmation")
    parser.add_argument("-f", "--file", type=str, required=True,
        help="Episodes FILE")
    parser.add_argument("path", type=str, metavar="FOLDER",
        help="FOLDER path")

    return parser.parse_args()

def check_mime(filename, mime):
    '''
    Check if file is of a certain mimetype.
    Return a boolean value.
    '''
    tmp = mimetypes.guess_type(filename)

    if tmp[0] and mime in tmp[0]:
        return True
    return False

def parse_file(filename):
    '''
    Read file name and return the number of season and episode.
    '''
    SxEy = re.compile('(s[0-9]+e[0-9]+|[0-9]+)', re.I)
    epnum = re.compile('[e0-9]([0-9]+)$', re.I)
    ssnum = re.compile('^(s[0-9]+|[0-9])', re.I)

    block = SxEy.search(filename).group().lower()

    ep = epnum.search(block).group()[1:]

    ss = ssnum.search(block).group()
    ss = ss[1:] if "s" in ss else ss

    return ep, ss

#
# Main
#
try:
    args = parse_cli()

    eps = []

    dir_list = os.listdir(args.path)
    dir_list.sort(key=lambda s: s.lower())

    vid = [ x for x in dir_list if check_mime(x, "video") ]
    sub = [ x for x in dir_list if check_mime(x, "text") ]

    with open(args.file) as arq:
        content = arq.read()
        lines = content.splitlines()

    c = 0
    run = True

    while( run ):
        run = False

        if c < len(vid):
            ep_num, ss_num = parse_file(vid[c])
            ep_name = lines[int(ep_num)-1]

            eps.append(Episode(
                ss_num, ep_num, ep_name, vid[c], args.path))

            run = True

        if c < len(sub):
            ep_num, ss_num = parse_file(sub[c])
            ep_name = lines[int(ep_num)-1]

            eps.append(Episode(
                ss_num, ep_num, ep_name, sub[c], args.path))

            run = True

        c += 1

    if not args.no_confirm:
        for c in range(0, len(eps)):
            print(eps[c])

        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            sys.exit(1)

    for c in range(0, len(eps)):
        eps[c].rename()

except (FileNotFoundError, OSError) as err:
    msg = "ERROR!\n{0} - {1}.".format(err.filename, err.strerror)
    exit_code = err.errno

except SystemExit as err:
    msg = "Exit\nExecution terminated by user."
    exit_code = err.code

else:
    msg = "Done!"
    exit_code = os.EX_OK

finally:
    print(msg)
    sys.exit(exit_code)
