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


#
# Import
#
import os
import re

from itertools import zip_longest
from shutil import move

from . import error


#
# Class
#
class LocalPath():
    def __init__(self, filename):
        self._curFileName = os.path.basename(filename)
        self._dirName = os.path.dirname(filename)
        self._fileNameExt = os.path.splitext(filename)[-1]
        self._newFileName = None

    @property
    def curFileName(self):
        return self._curFileName

    @property
    def dirName(self):
        return self._dirName

    @property
    def fileNameExt(self):
        return self._fileNameExt

    @property
    def newFileName(self):
        return self._newFileName

    @newFileName.setter
    def newFileName(self, newName):
        new = self._sanitizeName(newName)
        self._newFileName = "{}{}".format(new, self.fileNameExt)

    def rename(self):
        cur = os.path.join(self.dirName, self.curFileName)
        new = os.path.join(self.dirName, self._newFileName)
        if cur == new:
            strerr = ("Same file:\n"
                      "{}\n"
                      "{}.")
            raise error.SameFileError(strerr.format(cur, new))
        move(cur, new)

    def _sanitizeName(self, name):
        table = {
            ord("á"): "a",
            ord("à"): "a",
            ord("ã"): "a",
            ord("â"): "a",
            ord("é"): "e",
            ord("è"): "e",
            ord("ẽ"): "e",
            ord("ê"): "e",
            ord("í"): "i",
            ord("ì"): "i",
            ord("ĩ"): "i",
            ord("î"): "i",
            ord("ó"): "o",
            ord("ò"): "o",
            ord("õ"): "o",
            ord("ô"): "o",
            ord("ú"): "u",
            ord("ù"): "u",
            ord("ũ"): "u",
            ord("û"): "u",
            ord("ç"): "c",
            ord("ñ"): "n",
            ord(":"): " -",
            ord(">"): None,
            ord("<"): None,
            ord("?"): None,
            ord("!"): None,
            ord("*"): None,
            ord("#"): None,
            ord("/"): None,
            ord("\\"): None,
            ord("\""): None,
            ord("\'"): None
        }
        return name.translate(table)

    def _formatName(self, name):
        reSep = re.compile("[\W]+")
        reYear = re.compile("[12][0-9]{3}")
        reCountry = re.compile("[A-Z]{2}")
        countryCodes = [
            "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS",
            "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG",
            "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT",
            "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI",
            "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY",
            "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH",
            "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "UK",
            "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ",
            "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT",
            "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT",
            "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP",
            "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS",
            "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH",
            "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU",
            "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI",
            "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG",
            "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA",
            "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG",
            "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST",
            "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK",
            "TL", "TM", "TN", "TO", "TR", "TT", "TW", "TZ", "UA", "UG", "UM",
            "US", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU",
            "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"
        ]

        nameOnly = country = year = None
        tmp = name

        if reCountry.search(name):
            match = reCountry.findall(name)[0]

            if match in countryCodes:
                country = "GB" if match == "UK" else match
                tmp = reCountry.sub("", name)

        if reYear.search(name):
            match = reYear.findall(name)
            year = match[0]

        nameOnly = reSep.sub(" ", reYear.sub("", tmp)).strip()
        return {
            "title": nameOnly.title(),
            "country": country,
            "year": year
        }


class SerieFile(LocalPath):
    def __init__(self, filename):
        super().__init__(filename)
        rSceneRule = re.compile("[ .]S(\d{2})((E\d{2}-?)+)[ .]", re.I)
        rPreFormat = re.compile(" (\d{2})x((\d{2}-?)+) ")
        rAltFormat = re.compile("\.(\d{4}.)?(\d{3,})\.")

        if rSceneRule.search(self.curFileName):
            show, season, info = rSceneRule.split(self.curFileName)[:3]
            eps = re.findall("\d{2}", info)

        elif rPreFormat.search(self.curFileName):
            show, season, info = rPreFormat.split(self.curFileName)[:3]
            eps = re.findall("\d{2}", info)

        elif rAltFormat.search(self.curFileName):
            show, _, info = rAltFormat.split(self.curFileName)[:3]

            info_lst = list(info)
            info_lst.reverse()
            info_itr = [iter(info_lst)] * 2
            info_grp = zip_longest(*info_itr, fillvalue="0")
            info_lst = list(info_grp)
            s_num, s_dec = info_lst.pop()
            info_lst.reverse()

            season = "{}{}".format(s_dec, s_num)
            eps = ["{}{}".format(e_dec, e_num) for e_num, e_dec in info_lst]

        else:
            strerror = "Can't find show pattern for {}".format(self.curFileName)
            raise error.MatchNotFoundError(strerror)

        self._show = super()._formatName(show)
        self._show["season"] = "{:0>2}".format(season)
        self._show["episodes"] = eps
        self._identifier = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.identifier == other.identifier
        return False

    @property
    def country(self):
        return self._show.get("country")

    @property
    def episodes(self):
        return self._show.get("episodes")

    @property
    def season(self):
        return self._show.get("season")

    @property
    def title(self):
        return self._show.get("title")

    @property
    def year(self):
        return self._show.get("year")

    @property
    def identifier(self):
        if not self._identifier:
            identifier = re.sub("\W", "", self._show["title"])
            self._identifier = identifier.upper()
        return self._identifier
