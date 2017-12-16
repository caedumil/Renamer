# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


#
# Import
#
import logging

from . import types, error


#
# Global var
#
logger = logging.getLogger("Renamer.Web")


#
# Function
#
def genShowsDict(showFiles):
    showInfo = {}
    for show in set((x.title, x.country, x.year, x.identifier) for x in showFiles):
        try:
            logger.info("Downloading information for {0}.".format(show[0].upper()))
            showInfo[show[3]] = types.TvShow(show[0], show[1], show[2])

        except (error.DownloadError, error.NotFoundError) as err:
            logger.warn(err)
            showFiles = [x for x in showFiles if x.title != show[0]]

    if not showInfo:
        raise error.NotFoundError("Could not download episode's names for any show")

    return showInfo


def populateShows(showInfo):
    for show in showInfo.values():
        logger.info("Downloading episodes list for {0}.".format(show.title))
        show.populate()
