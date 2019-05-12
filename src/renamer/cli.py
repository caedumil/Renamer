# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import argparse

from . import __version__


def setParser():
    parser = argparse.ArgumentParser(prog='renamer')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s v{}'.format(__version__)
    )
    parser.add_argument(
        '-y',
        '--yes',
        action='store_true',
        help='Automatically accept all changes.'
    )
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help='Recursively descend into directories.'
    )
    parser.add_argument(
        '-l',
        '--loglevel',
        metavar='LEVEL',
        default='INFO',
        type=str,
        choices=['INFO', 'WARN', 'ERROR', 'DEBUG'],
        help='Set log level (INFO, WARN, ERROR).'
    )
    parser.add_argument(
        'path',
        type=str,
        metavar='FILE',
        nargs='+',
        help='FILE location.'
    )
    return parser
