# Copyright (c) 2021, Carlos Millett
# All rights reserved.

# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
from pathlib import Path

from .base import Media
from .types import Types


class Series(Media):
    _rSceneRule = re.compile(r'[ .]S(\d{2})((?:E\d{2}-?)+)[ .]', re.I)
    _rPreFormat = re.compile(r'(?: -)? (\d{2})x((?:\d{2}-?)+) (?: -)?')

    def __init__(self, path: Path) -> None:
        super().__init__(Types.SERIES, path)

    @classmethod
    def match(cls, filename: str) -> bool:
        if cls._rSceneRule.search(filename):
            return True
        elif cls._rPreFormat.search(filename):
            return True
        return False

    @classmethod
    def parse(cls, filename: str) -> str:
        if cls._rSceneRule.search(filename):
            return cls._rSceneRule.split(filename)[0]
        elif cls._rPreFormat.search(filename):
            return cls._rPreFormat.split(filename)[0]
        return ''