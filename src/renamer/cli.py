# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import argparse
from pathlib import Path

from . import __version__


def setParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='renamer')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s v{}'.format(__version__)
    )
    parser.add_argument(
        '-l',
        '--loglevel',
        metavar='LEVEL',
        default='INFO',
        type=str.upper,
        choices=['INFO', 'WARN', 'ERROR', 'DEBUG'],
        help='Set log level (INFO, WARN, ERROR).'
    )
    parser.add_argument(
        '-s',
        '--season',
        default=-1,
        type=int,
        help='force SEASON number to the specified value.'
    )
    parser.add_argument(
        '--no-confirm',
        action='store_false',
        dest='askuser',
        help='Do not prompt before rename.'
    )
    parser.add_argument(
        'path',
        type=Path,
        metavar='FILE',
        nargs='+',
        help='FILE location.'
    )
    return parser
