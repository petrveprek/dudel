#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""

import argparse, sys, time

TITLE = "Duplicate Delete"
VERSION = "0.1"
VERBOSE = False

def now(on="on", at="at"):
    return "{}{} {}{}".format(
        on + " " if on != "" else "", time.strftime("%Y-%m-%d"),
        at + " " if at != "" else "", time.strftime("%H:%M:%S"))

def main():
    print("{} {}".format(TITLE, VERSION))
    if VERBOSE:
        print("\a", end="")
        print("Python {}".format(sys.version))
        print("Command '{}'".format(sys.argv[0]))
        print("Arguments {}".format(sys.argv[1:]))
        print("Executed {}".format(now()))
        start = time.time()
    
    parser = argparse.ArgumentParser(description="delete dups")
    parser.add_argument("-c", "--common", help="shared")
    subparsers = parser.add_subparsers(help="sub-command help")
    parserOneDir = subparsers.add_parser("dir", help="help1")
    parserOneDir.add_argument("-1", "--one", help="opt1")
    parserTwoDirs = subparsers.add_parser("dir1 dir2", help="help2")
    parserTwoDirs.add_argument("-2", "--two", help="opt2")
## create the parser for the "a" command
#parser_a = subparsers.add_parser('a', help='a help')
#parser_a.add_argument("--opt1", action='store_true')
#parser_a.add_argument("--opt2", action='store_true')
#
## create the parser for the "b" command
#parser_b = subparsers.add_parser('b', help='b help')
#parser_b.add_argument("--opt3", action='store_true')
#parser_b.add_argument("--opt4", action='store_true')
#xx
#---    parser.add_argument("directory", nargs="?", help="set top directory to analyze [%(default)s]", default=os.getcwd())
#---    parser.add_argument("-c", "--count", help="set number of largest directories to show [%(default)s]", type=int, default=COUNT)
#---    parser.add_argument("-w", "--width", help="set console width for progress indicator [%(default)s]", metavar="<{},{}>".format(MIN_WIDTH,MAX_WIDTH), type=int, choices=range(MIN_WIDTH,MAX_WIDTH+1), default=WIDTH)
#---    parser.add_argument("-s", "--silent", help="suppress progress messages [false]", action = "store_true", default=False)
    arguments = parser.parse_args()
#---    directory = arguments.directory
#---    count = arguments.count
#---    width = arguments.width
#---    silent = arguments.silent
    
    if VERBOSE:
        elapsed = time.time() - start
        seconds = round(elapsed)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        print("Completed {}".format(now()))
        print("Elapsed {:d}w {:d}d {:d}h {:d}m {:d}s ({:,.3f}s)".format(weeks, days, hours, minutes, seconds, elapsed))
    print("\a", end="")

if '__main__' == __name__:
    main()

# dudel directory
# dudel master inspect (when several file copies exist, keep the ones (even multiple) in master directory, delete all from inspect directory)
# --find unique/duplicate(multiple)
# --type(target) file/directory
# --match filename/extension/datetime/size/sha1-crc32-md5/content(byte-by-byte)
# --action list(show)/delete/move/rename
# --mode
#? keep MASTER reference original prototype source exemplar
#? prune check search COPY target
#? match sub-tree / file name / extension / date-time / size / content
#? sh1 / md5 ... byte-by-byte (identical)
#? interactive mode
#? find unique|dup files|directories
#? do not delete, show only | move to | rename
#? action: list/show, delete, rename?, move?
#? sys.stdout.isatty() --> if not, then no progress or no backtrack
#? no progress, silent
#? a] master
#? b] master copy
# prune / sort / save md5 et al / keep empty dirs / STATS
