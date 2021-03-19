# Copyright (c) 2021, Carlos Millett
# All rights reserved.

# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re
from pathlib import Path

from .base import Media
from .types import Types


class Animes(Media):
    _rRule = re.compile('')

    def __init__(self, path: Path) -> None:
        super().__init__(Types.ANIMES, path)

    @classmethod
    def match(cls, filename: str) -> bool:
        return False

    @classmethod
    def parse(cls, filename: str) -> str:
        return ''
