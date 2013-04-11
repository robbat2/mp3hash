#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import logging
import hashlib
from optparse import OptionParser

from mp3hash import mp3hash


# hashlib.algorithms was included in python 2.7
ALGORITHMS = getattr(
    hashlib,
    'algorithms',
    ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
)

_LOGGING_FMT_ = '%(asctime)s %(levelname)-8s %(message)s'


def error(msg, is_exit=True):
    logging.error(msg)
    if is_exit:
        sys.exit()


def list_algorithms():
    print(u'\n'.join(ALGORITHMS))


def main():
    opts, args, parser = parse_arguments()

    if not args and not opts.list_algorithms:
        parser.print_help()
        print
        error(u"Insufficient arguments")

    if opts.maxbytes is not None and opts.maxbytes <= 0:
        parser.print_help()
        print
        error(u"Invalid value for --maxbytes it should be a positive integer")

    if opts.list_algorithms:
        list_algorithms()
        sys.exit(0)

    if opts.algorithm not in ALGORITHMS:
        error(u"Unkown '{}' algorithm. Available options are: {}"
              .format(opts.algorithm, ", ".join(ALGORITHMS)))

    for arg in args:
        path = os.path.realpath(arg)
        if not os.path.isfile(path):
            error(u"File at '{}' does not exist or it is not a regular file"
                  .format(arg))
            continue

        hasher = hashlib.new(opts.algorithm)

        print mp3hash(path, maxbytes=opts.maxbytes, hasher=hasher),  # No \n
        print os.path.basename(path) if not opts.hash else ''


def parse_arguments():
    parser = OptionParser()

    parser.add_option("-a", "--algorithm", default='sha1',
                      help="Hash algorithm to use. Default sha1.  "
                      "See --list-algorithms")

    parser.add_option("-l", "--list-algorithms", action="store_true",
                      default=False, help="List available algorithms")

    parser.add_option("-q", "--hash", action="store_true", default=False,
                      help="Print only hash information, no filename")

    parser.add_option("-m", "--maxbytes", type=int, default=None,
                      help="Max number of bytes of music to hash")

    parser.add_option("-o", "--output", default=False,
                      help="Redirect output to a file")

    parser.add_option("-v", "--verbose", action="count", default=0)

    parser.set_usage("Usage: [options] FILE [FILE ..]")

    (opts, args) = parser.parse_args()

    return opts, args, parser


def configure_logging(verbose):
    logging_levels = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    level = logging_levels[verbose if verbose < 3 else 2]
    logging.basicConfig(level=level, format=_LOGGING_FMT_)


def configure_output(output):
    if output:
        stdout = sys.stdout
        try:
            sys.stdout = open(output, 'w')
        except IOError, err:
            sys.stdout = stdout
            error(u"Couldn't open {}: {}".format(output, err))


if __name__ == "__main__":
    main()