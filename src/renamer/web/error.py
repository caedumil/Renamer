# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


#
# Exception
#
class DownloadError(Exception):
    '''Raise when page cannot be downloaded.'''


class NotFoundError(Exception):
    '''Raise when show can't be found in the remote database.'''
