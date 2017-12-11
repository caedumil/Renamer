import argparse

from renamer import __version__


def setParser():
    parser = argparse.ArgumentParser(prog="renamer")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s v{}".format(__version__)
    )
    parser.add_argument(
        "-y",
        "--no-confirm",
        action="store_true",
        help="Do not ask for confirmation."
    )
    parser.add_argument(
        "-s",
        "--simple",
        action="store_true",
        help="Omit show title from filename."
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively descend into directories."
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        metavar="LEVEL",
        default="INFO",
        type=str,
        choices=["INFO", "WARN", "ERROR"],
        help="Set log level (INFO, WARN, ERROR)."
    )
    parser.add_argument(
        "path",
        type=str,
        metavar="FILE",
        nargs="+",
        help="FILE location."
    )

    return parser
