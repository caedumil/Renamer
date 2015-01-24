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
class Episode():
    '''
    Represents the episode file on disk.
    '''
    def __init__(self, ename, fname, fpath):
        self.full_ename = "{}.{}".format(ename, fname.split(".")[-1])
        self.filename = fname
        self.path = fpath

    def __str__(self):
        return ">>> {0}\n<<< {1}".format(self.filename, self.full_ename)

    def rename(self):
        '''
        Rename the file.
        '''
        self.fname_on_disk = os.path.join(self.path, self.filename)
        self.ename_on_disk = os.path.join(self.path, self.full_ename)

        os.rename(self.fname_on_disk, self.ename_on_disk)

#
# Functions
#
def parse_cli():
    '''
    Set and parse command-line arguments.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s -- dev build")
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

def get_new_name(names_list, filename):
    '''
    Parse filename to get values for episode and season numbers and
    find the correct string to rename the file.
    '''
    SxEy = re.compile('(\.\d{4})?\.(\.?\d{1,2}\.\d{2,}|\d{3,})\.', re.I)
    xy = re.compile('(0[1-9]|[1-9][0-9]?)\.?([0-9]{2,})')

    comm = (lambda x: True if re.search('^#\w?', x, re.I) else False)

    namestring = re.sub('[^0-9]', '.', filename)
    pair = xy.search(SxEy.search(namestring).group(2))

    ss_num, ep_num = pair.groups() if pair else ("WW", "YY")
    ep_name = (
        names_list[int(ep_num)-1] if ep_num.isdecimal() else "..."
        )

    if int(ep_num) < len(names_list) and comm(names_list[int(ep_num)]):
        ep_num = "{:0>2}-{:0>2}".format(ep_num, int(ep_num)+1)

    return "{0}x{1} - {2}".format(ss_num, ep_num, ep_name)

#
# Main
#
args = parse_cli()

exit_msg = "Done!"
exit_code = os.EX_OK

try:
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
            eps.append(Episode(get_new_name(lines, vid[c]), vid[c], args.path))

            run = True

        if c < len(sub):
            eps.append(Episode(get_new_name(lines, sub[c]), sub[c], args.path))

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

except (OSError, IOError) as err:
    exit_msg = "ERROR!\n{0} - {1}.".format(err.filename, err.strerror)
    exit_code = err.errno

except SystemExit as err:
    exit_msg = "Exit\nExecution terminated by user."
    exit_code = err.code

finally:
    print(exit_msg)
    sys.exit(exit_code)
