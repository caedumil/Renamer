# Copyright (c) 2021, Carlos Millett
# All rights reserved.

# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
from pathlib import Path

from .base import Media
from .types import Types


class Movies(Media):
    _rScene = re.compile(r'([\w\.\-\ ]+[12][0-9]{3})\.')

    def __init__(self, path: Path) -> None:
        super().__init__(Types.MOVIES, path)

    @classmethod
    def match(cls, filename: str) -> bool:
        if cls._rScene.search(filename):
            return True
        return False

    @classmethod
    def parse(cls, filename: str) -> str:
        if cls._rScene.search(filename):
            return cls._rScene.split(filename)[1]
        return ''
