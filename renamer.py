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

# Classes definitions
class Episode():
    def __init__(self, season, episode, name):
        self.season = season
        self.episode = episode
        self.name = name

    def get_name(self, extension="new"):
        self.ext = extension

        return "{0}x{1} - {2}.{3}".format(
            self.season, self.episode, self.name, self.ext)

class LFile():
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.ext = filename.split(".")[-1]

    def rename(self, epname):
        self.epname = epname
        self.fullfname = os.path.join(self.path, self.filename)
        self.fullename = os.path.join(self.path, self.epname)

        os.rename(self.fullfname, self.fullename)

# Command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--season", type=int, required=True,
    help="Season number")
parser.add_argument("-p", "--path", type=str, required=True,
    help="Folder PATH")
parser.add_argument("-f", "--file", type=str, required=True,
    help="Episodes FILE")
parser.add_argument("--no-confirm", action="store_true",
    help="Don not ask for confirmation")
args = parser.parse_args()

# Initialize lists
eps = []
vid = []
sub = []

# Get all files inside the directory
# Sort list of files, case insensitive
# Use the files to create LFiles objects
# Append videos file object to vid list
# Append subtitle file object to sub list
dir_list = os.listdir(args.path)
dir_list.sort(key=lambda s: s.lower())

for fl in dir_list:
    if ".srt" in fl:
        sub.append(LFile(fl, args.path))
    else:
        vid.append(LFile(fl, args.path))

# Use regular expression to parse the file
# Read and parse the file content
# Append Episode objects to eps list
regex = re.compile('; ')

try:
    with open(args.file) as arq:
        while(True):
            line = arq.readline()
            if not line:
                break

            ep_num, ep_name = regex.split(line)
            ep_name = ep_name.replace("\n", "")

            eps.append(Episode("%02i"%args.season, ep_num, ep_name))

except FileNotFoundError as err:
    print("ERROR!")
    print("{0} - {1}".format(err.filename, err.strerror))
    sys.exit(err.errno)

# Print changes to stdout if confirmation is set
# Ask to proceed
if not args.no_confirm:
    for c in range(0, len(eps)):
        print("<<< {0}\n>>> {1}".format(
            vid[c].filename, eps[c].get_name(vid[c].ext)))

    anws = input("Apply changes? [Y/n]: ")
    if anws in ["N", "n"]:
        print("Aborting now.")
        sys.exit(1)

# Apply name changes to all files
try:
    for c in range(0, len(eps)):
        if sub:
            sub[c].rename(eps[c].get_name(sub[c].ext))
        vid[c].rename(eps[c].get_name(vid[c].ext))

except OSError as err:
    print("ERROR!")
    print("{0} - {1}".format(err.filename, err.strerror))
    sys.exit(err.errno)

else:
    print("Done")
    sys.exit(os.EX_OK)
