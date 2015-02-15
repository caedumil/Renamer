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


class Filenames():
    '''
    Holds a list of strings to form a new episode name.
    '''
    def __init__(self, ep_list):
        self.names = ep_list
        self.length = len(ep_list)
        self.patt1 = '(\.\d{4})?\.(\.?\d{1,2}\.\d{2,}|\d{3,})\.'
        self.patt2 = '(0[1-9]|[1-9][0-9]?)\.?([0-9]{2,})'

    def __validate_ep(self, ep):
        __num = ep

        if ep < self.length and re.search('^#\w?', self.names[ep]):
            __num = "{:0>2}-{:0>2}".format(ep, ep+1)

        return __num

    def new_name(self, filename):
        '''
        Extract information from the filename and return a formatted string to
        use as new filename.
        '''
        __namestr = re.sub('[^0-9]', '.', filename)
        __find = re.search(self.patt1, __namestr).group(2)
        __pair = re.search(self.patt2, __find)

        if __pair:
            __ss, __ep = __pair.group(1), int(__pair.group(2))
            __name = self.names[__ep-1]

            __ep = self.__validate_ep(__ep)

            return "{0:0>2}x{1:0>2} - {2}".format(__ss, __ep, __name)

        return None

#
# Main
#
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s -- dev build")
    parser.add_argument("--no-confirm", action="store_true",
        help="Do not ask for confirmation")
    parser.add_argument("epnames", type=str, metavar="LIST",
        help="Text file with the LIST of episode's names")
    parser.add_argument("path", type=str, metavar="FOLDER",
        help="FOLDER with episodes files")

    args = parser.parse_args()

    exit_msg = "Done!"
    exit_code = os.EX_OK

    try:
        files = os.listdir(args.path)

        with open(args.epnames) as arq:
            content = arq.read()
            lines = content.splitlines()
            names = Filenames(lines)

        names = { x:names.new_name(x) for x in files }

        eps = [ Episode(y, x, args.path) for x,y in names.items() if y ]
        eps.sort(key=lambda x: x.full_ename)

        if not args.no_confirm:
            for ep in eps:
                print(ep)

            anws = input("Apply changes? [Y/n]: ")
            if anws in ["N", "n"]:
                sys.exit(1)

        for ep in eps:
            ep.rename()

    except (OSError, IOError) as err:
        exit_msg = "ERROR!\n{0} - {1}.".format(err.filename, err.strerror)
        exit_code = err.errno

    except SystemExit as err:
        exit_msg = "Exit\nExecution terminated by user."
        exit_code = err.code

    finally:
        print(exit_msg)
        sys.exit(exit_code)
