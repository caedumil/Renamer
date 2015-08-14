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
import shutil
import difflib
import urllib.request
import xml.etree.ElementTree as etree

#
# Classes
#
class Show():
    '''
    TV show information.

    Fetch data online, using TVRage API.
    Keep the episode list of specified TV show and season.
    '''
    def __init__(self, showname, season=None):
        self.showname = showname
        self.showid = self.__getID()
        self.__getEpList()

        if season:
            self.setSeason(season)

    def __fuzzyMatch(self, names):
        match = difflib.get_close_matches(self.showname, names)

        return match[0]

    def __getID(self):
        url= "http://services.tvrage.com/feeds/search.php?show="
        down = urllib.request.urlopen(url + self.showname)
        data = down.read()

        root = etree.fromstring(data.decode("UTF-8"))

        show = zip(root.findall("show/name"), root.findall("show/showid"))
        show = { x.text.lower():y.text for x, y in show }

        match = self.__fuzzyMatch(show.keys())

        return show[match]

    def __getEpList(self):
        url = "http://services.tvrage.com/feeds/episode_list.php?sid="
        down = urllib.request.urlopen(url + self.showid)
        data = down.read()

        root = etree.fromstring(data.decode("UTF-8"))
        self.__xml = root.find("Episodelist")

    def __readXML(self, season):
        item = "Season[@no='{0}']/episode/".format(season.lstrip("0"))

        eps = [ x.text for x in self.__xml.findall(item + "seasonnum") ]
        titles = [ x.text for x in self.__xml.findall(item + "title") ]

        return { x:y for (x, y) in zip(eps, titles) }

    def setSeason(self, season):
        '''
        Set the season number to store episodes list.
        '''
        self.ep_title = { x:self.__readXML(x) for x in season }

    def getTitle(self, season, ep):
        '''
        Return the ep title of the show.
        '''
        return self.ep_title[season][ep]

class Folder():
    '''
    File information.

    Parse the filename to get:
        - show name
        - season number
        - episode number

    If fails to find, value is set to None.
    '''
    def __init__(self, path, target, filename):
        self.path = path
        self.target = target if target else path
        self.filename = filename
        self.show = self.__getName()

        if self.show:
            self.season, self.episode = self.__getNumbers()
            self.epname = "{0}x{1}".format(self.season, self.episode)

    def __getName(self):
        regex = re.compile("([\w. -]+?([. ][12]\d{3})?)[. ]([Ss]\d{2}|\d{3})")
        name = regex.search(self.filename)

        return name.group(1).lower() if name else None

    def __getNumbers(self):
        rtail = re.compile("(\d)[. ].*")
        rnumbers = re.compile("(\d{2})(\d{2})")

        name = re.sub(self.show, "", self.filename, flags=re.I)

        name = rtail.sub(lambda x: x.group(1), name)
        name = re.sub("[^0-9]", "", name)

        if (len(name) % 2) != 0:
            name = "0" + name

        nums = rnumbers.search(name)

        if not nums:
            return None, None

        return nums.group(1), nums.group(2)

    def setEpName(self, name):
        '''
        Use name to set the new filename.
        '''
        _, ext = os.path.splitext(self.filename)
        proper = name.replace("/", "-")
        self.epname = "{0} - {1}{2}".format(self.epname, proper, ext)

    def addShowName(self):
        self.epname = "{0} - {1}".format(self.show, self.epname)

    def rename(self):
        '''
        Rename the file on disk.
        '''
        fname = os.path.join(self.path, self.filename)
        ename = os.path.join(self.target, self.epname)

        shutil.move(fname, ename)

#
# Main
#
def __main():
    files = []
    uniq = []

    for path in args.path:
        if os.path.isdir(path):
            files += [ Folder(path, args.target, x) for x in os.listdir(path) ]

        else:
            pth, ep = os.path.split(path)
            if not pth:
                pth = os.path.curdir

            files += [ Folder(pth, args.target, ep) ]

    files = [ x for x in files if x.show ]

    for show in set( x.show for x in files ):
        uniq.append( (show, set( x.season for x in files if show == x.show )) )

    names = {}
    for show, seasons in uniq:
        print("Fetching episodes for: {0}".format(show.title()))
        names[show] = Show(show, seasons)

    for f in files:
        f.setEpName(names[f.show].getTitle(f.season, f.episode))

    if args.show_name:
        for f in files:
            f.addShowName()

    files.sort(key=lambda x: x.epname)

    if not args.no_confirm:
        for ep in files:
            print("<<< {0}\n>>> {1}".format(ep.filename, ep.epname))

        anws = input("Apply changes? [Y/n]: ")
        if anws in ["N", "n"]:
            sys.exit(1)

    for ep in files:
        ep.rename()

#
# Execute code
#
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="version",
        version="%(prog)s -- 0.10-dev")
    parser.add_argument("--no-confirm", action="store_true",
        help="Do not ask for confirmation")
    parser.add_argument("--show-name", action="store_true",
        help="Prepend the show name to the filename")
    parser.add_argument("-t", "--target", type=str, default=None,
        help="Destination folder")
    parser.add_argument("path", type=str, metavar="FOLDER", nargs="+",
        help="FOLDER with episodes files")

    args = parser.parse_args()

    exit_msg = "Done!"
    exit_code = os.EX_OK

    try:
        __main()

    except OSError as err:
        exit_msg = "ERROR!\n{0} - {1}.".format(err.filename, err.strerror)
        exit_code = err.errno

    except SystemExit as err:
        exit_msg = "Exit\nExecution terminated by user."
        exit_code = err.code

    except Exception as err:
        exit_msg = "{0}\n{1}".format(type(err), err)

    finally:
        print(exit_msg)
        sys.exit(exit_code)
