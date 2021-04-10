# Copyright (c) 2021, Carlos Millett
# All rights reserved.

# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
from pathlib import Path

from .base import Media
from .types import Types


class Animes(Media):
    _rRule = re.compile(r'\[.+\] ([\w\.\-\ ]+?)(?: S(\d))? - (\d{2,})')

    def __init__(self, path: Path) -> None:
        super().__init__(Types.ANIMES, path)

    @classmethod
    def match(cls, filename: str) -> bool:
        if cls._rRule.search(filename):
            return True
        return False

    @classmethod
    def parse(cls, filename: str) -> str:
        if cls._rRule.search(filename):
            return cls._rRule.split(filename)[1]
        return ''

    @classmethod
    def format(cls, filename: str) -> str:
        info = cls._rRule.search(filename)
        if not info:
            return ''

        title, season, ep = info.groups()
        if not season:
            season = '01'

        return '{0} - S{1:0>2}E{2}'.format(title, season, ep)
