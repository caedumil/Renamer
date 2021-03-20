# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


from . import cli
from .utils import (
    setupLogger,
    genFilesList,
    matchFiles,
    processFiles
)


def main():
    parser = cli.setParser()
    args = parser.parse_args()
    logger = setupLogger(args.loglevel)

    filesList = genFilesList(args.path)
    filesList = matchFiles(filesList)
    processFiles(filesList)


if __name__ == '__main__':
    main()
