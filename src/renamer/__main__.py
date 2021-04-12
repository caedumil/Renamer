# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


from .cli import setParser
from .errors import (
    CancelledByUserError,
    EmptyListError
)
from .utils import (
    setupLogger,
    genFilesList,
    matchFiles,
    processFiles
)


def main() -> None:
    parser = setParser()
    args = parser.parse_args()
    logger = setupLogger(args.loglevel)

    try:
        filesList = genFilesList(args.path)
        matchedList = matchFiles(filesList)
        processFiles(matchedList, args.season, args.askuser)

    except EmptyListError as err:
        files = ['\t{0}'.format(x.resolve()) for x in err.files]
        message = "{0}\n{1}".format(err.message, '\n'.join(files))
        logger.error(message)

    except CancelledByUserError as err:
        logger.info(err.message)

    return


if __name__ == '__main__':
    main()
