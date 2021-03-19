# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.

import sys

from renamer import cli
from renamer import log


def main():
    parser = cli.setParser()
    args = parser.parse_args()
    logger = log.setupLogger()

    return cli.main(args, logger)


if __name__ == '__main__':
    sys.exit(main())
