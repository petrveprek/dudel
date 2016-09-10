#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""

import argparse, os, string, sys, time

TITLE = "Duplicate Delete"
VERSION = "0.1"
VERBOSE = False
MIN_WIDTH = 9+0+3 # intro + directory + ellipsis
MAX_WIDTH = os.get_terminal_size().columns if sys.stdout.isatty() else 80
WIDTH = MAX_WIDTH
WIDTH = min(max(WIDTH, MIN_WIDTH), MAX_WIDTH)

def now(on="on", at="at"):
    return "{}{} {}{}".format(
        on + " " if on != "" else "", time.strftime("%Y-%m-%d"),
        at + " " if at != "" else "", time.strftime("%H:%M:%S"))

def printable(str, max):
    str = "".join([char if char in string.printable else "_" for char in str])
    if len(str) > max: str = str[:max-3] + "..."
    return str

def main():
    print("{} {}".format(TITLE, VERSION))
    if VERBOSE:
        print("\a", end="")
        print("Python {}".format(sys.version))
        print("Command '{}'".format(sys.argv[0]))
        print("Arguments {}".format(sys.argv[1:]))
        print("Executed {}".format(now()))
        start = time.time()
    
    parser = argparse.ArgumentParser(description="Finds and deletes duplicate files located under top `directory`.")
    parser.add_argument("directory", nargs="?", help="set top directory to clean up [%(default)s]", default=os.getcwd())
    parser.add_argument("-w", "--width", help="set console width for progress indicator [%(default)s]", metavar="<{},{}>".format(MIN_WIDTH,MAX_WIDTH), type=int, choices=range(MIN_WIDTH,MAX_WIDTH+1), default=WIDTH)
    parser.add_argument("-s", "--silent", help="suppress progress messages [false]", action = "store_true", default=False)
    arguments = parser.parse_args()
    directory = arguments.directory
    width = arguments.width
    silent = arguments.silent
    
    if not silent:
        print("Analyzing {}".format(directory))
        BACKTRACK = ("\r" if width < MAX_WIDTH else "\033[F") if sys.stdout.isatty() else "\n"
    for path, dirs, files in os.walk(directory):
        if not silent:
            print("Scanning {: <{}}".format(printable(path, width-9), width-9), end=BACKTRACK)
    if not silent:
        print("         {: <{}}".format("", width-9), end=BACKTRACK)
    
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
