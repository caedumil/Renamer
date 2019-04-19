# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


from collections import namedtuple


Provider = namedtuple('Provider', ['url'])

Show = namedtuple(
    'Show',
    [
        'title',
        'country',
        'premier',
        'thetvdb',
        'image',
        'episodes'
    ]
)

Episode = namedtuple(
    'Episode',
    [
        'name',
        'season',
        'number',
        'airdate',
        'image'
    ]
)
