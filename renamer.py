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

# Classes definitions
class LFile():
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.ext = filename.split(".")[-1]

    def rename(self, ename):
        self.full_fname = os.path.join(self.path, self.filename)
        self.full_ename = os.path.join(self.path, ename)

        os.rename(self.full_fname, self.full_ename)

class Episode(LFile):
    def __init__(self, season, enumber, ename, fname, fpath):
        super().__init__(fname, fpath)
        self.season = "%02i"%(int(season))
        self.enumber = "%02i"%(int(enumber))
        self.ename = ename
        self.full_ename = "{0}x{1} - {2}.{3}".format(
            self.season, self.enumber, self.ename, super().ext)

    def rename(self):
        super().rename(self.full_ename)

    def ___str___(self):
        return ">>> {0}\n<<< {1}".format(super().filename, self.full_ename)

# Command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--no-confirm", action="store_true",
    help="Don not ask for confirmation")
parser.add_argument("-s", "--season", type=int, required=True,
    help="Season number")
parser.add_argument("-f", "--file", type=str, required=True,
    help="Episodes FILE")
parser.add_argument("path", type=str, metavar="FOLDER",
    help="FOLDER path")

args = parser.parse_args()

# Initialize lists
eps_v = []
eps_s = []
vid = []
sub = []

# Get all files inside the directory
# Sort list of files, case insensitive
# Use the files to create separate lists for video
# and subtitles
#
# Use regular expression to parse the file
# Read and parse the file content
# Append Episode objects to eps_* list
#
# Print changes to stdout if confirmation is set
# Ask to proceed
# Apply name changes to all files
regex = re.compile('; ')

try:
    dir_list = os.listdir(args.path)
    dir_list.sort(key=lambda s: s.lower())

    vid = [ x for x in dir_list if "video" in mimetypes.guess_type(x)[0] ]
    sub = [ x for x in dir_list if "text" in mimetypes.guess_type(x)[0] ]

    with open(args.file) as arq:
        c = 0

        while(True):
            line = arq.readline()
            if not line:
                break

            ep_num, ep_name = regex.split(line)
            ep_name = ep_name.replace("\n", "")

            eps_v.append(Episode(
                args.season, ep_num, ep_name, vid[c], args.path))
            eps_s.append(Episode(
                args.season, ep_num, ep_name, sub[c], args.path))

            c += 1

    if not args.no_confirm:
        for c in range(0, len(eps)):
            print(eps_v[c])
            if sub:
                print(eps_s[c])

        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            print("Aborting now.")
            sys.exit(1)

    for c in range(0, len(eps_v)):
        if sub:
            eps_s[c].rename()
        eps_v[c].rename()

except (FileNotFoundError, OSError) as err:
    print("ERROR!")
    print("{0} - {1}".format(err.filename, err.strerror))
    exit_code = err.errno

except ValueError:
    print("ERROR!")
    print("Missing field in {} file".format(args.file))
    exit_code = 1

else:
    print("Done")
    exit_code = os.EX_OK

finally:
    sys.exit(exit_code)
