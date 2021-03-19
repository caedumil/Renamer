# Copyright (c) 2021, Carlos Millett
# All rights reserved.

# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import abc
from pathlib import Path

from .types import Types


class Media(abc.ABC):
    def __init__(self, media_type: Types, path: Path) -> None:
        self._type: Types = media_type
        self._path: Path = path
        self._title: str = ''
        self._folder: str = ''

    @property
    def type(self) -> Types:
        return self._type

    @property
    def path(self) -> Path:
        return self._path

    @property
    def title(self) -> str:
        if not self._title:
            self._title = self.parse(self._path.name)
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def folder(self) -> str:
        return self._folder

    @folder.setter
    def folder(self, folder: str) -> None:
        self._folder = folder

    @classmethod
    @abc.abstractmethod
    def match(cls, filename: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def parse(cls, filename: str) -> str:
        pass
