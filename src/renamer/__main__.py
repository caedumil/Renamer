# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


from . import cli
from . import log


def main():
    parser = cli.setParser()
    args = parser.parse_args()
    logger = log.setupLogger(args.loglevel)

    return cli.main(args, logger)


if __name__ == '__main__':
    main()
