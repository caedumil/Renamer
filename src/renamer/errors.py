# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


from typing import (
    Any,
    List
)


class Error(Exception):
    pass


class EmptyListError(Error):
    def __init__(self, message: str, files: List[Any]) -> None:
        self.message = message
        self.files = files


class CancelledByUserError(Error):
    def __init__(self, message: str) -> None:
        self.message = message
