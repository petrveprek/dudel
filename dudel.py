#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""
#? keep MASTER reference original prototype source exemplar
#? prune check search COPY target
#? match sub-tree / filename / date-time / size / content
#? do not delete, show only
#? action: list/show, delete, rename?, move?
#? sys.stdout.isatty() --> if not, then no progress or no backtrack
#? no progress, silent
#? a] master
#? b] master copy
#
# dius
# .] mk DEVELOP
# 1ST
# 1] MAX_WIDTH = os.get_terminal_size().columns if sys.stdout.isatty() else 80
# 2] BACKTRACK = ("\r" if width < MAX_WIDTH else "\033[F") if sys.stdout.isatty() else "\n"
# 2ND
# -s --silent
# .] 1.1, readme, changelog
#

import sys, time
#--- argparse, enum, math, os, string

TITLE = "Duplicate Delete"
VERSION = "0.1"
VERBOSE = False
#---COUNT = 20
#---class Mode(enum.Enum): plain = 0; grouped = 1; gazillion = 2
#---MODE = Mode.gazillion
#---MIN_WIDTH = 9+0+3 # intro + directory + ellipsis
#---MAX_WIDTH = os.get_terminal_size().columns
#---WIDTH = MAX_WIDTH
#---WIDTH = min(max(WIDTH, MIN_WIDTH), MAX_WIDTH)

def now(on="on", at="at"):
    return "{}{} {}{}".format(
        on + " " if on != "" else "", time.strftime("%Y-%m-%d"),
        at + " " if at != "" else "", time.strftime("%H:%M:%S"))

#---def printable(str, max):
#---    str = "".join([char if char in string.printable else "_" for char in str])
#---    if len(str) > max: str = str[:max-3] + "..."
#---    return str
#---
#---def plain(num):
#---    return "{}".format(num)
#---
#---def grouped(num):
#---    return "{:,}".format(num)
#---
#---def gazillion(num, suffix="B"):
#---    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
#---        if num < 1024.0:
#---            return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, unit, suffix)
#---        num /= 1024.0
#---    return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, 'Yi', suffix)
#---
#---def format(num, mode=Mode.plain):
#---    return(
#---        grouped(num)   if mode == Mode.grouped   else
#---        gazillion(num) if mode == Mode.gazillion else
#---        plain(num))
#---
#---def places(num, min=0, mode=Mode.plain):
#---    return max(min, len(format(num, mode)))

def main():
    print("{} {}".format(TITLE, VERSION))
    if VERBOSE:
        print("\a", end="")
        print("Python {}".format(sys.version))
        print("Command '{}'".format(sys.argv[0]))
        print("Arguments {}".format(sys.argv[1:]))
        print("Executed {}".format(now()))
        start = time.time()
    
#---    parser = argparse.ArgumentParser()
#---    parser.add_argument("directory", nargs="?", help="set top directory to analyze [%(default)s]", default=os.getcwd())
#---    parser.add_argument("-c", "--count", help="set number of largest directories to show [%(default)s]", type=int, default=COUNT)
#---    parser.add_argument("-w", "--width", help="set console width for progress indicator [%(default)s]", metavar="<{},{}>".format(MIN_WIDTH,MAX_WIDTH), type=int, choices=range(MIN_WIDTH,MAX_WIDTH+1), default=WIDTH)
#---    arguments = parser.parse_args()
#---    directory = arguments.directory
#---    count = arguments.count
#---    width = arguments.width
#---    
#---    print("Analyzing {}".format(directory))
#---    started = time.time()
#---    usage = {}
#---    numFiles = 0
#---    backtrack = "\r" if width < MAX_WIDTH else "\033[F"
#---    for path, dirs, files in os.walk(directory):
#---        print("Scanning {: <{}}".format(printable(path, width-9), width-9), end=backtrack)
#---        files = list(filter(os.path.isfile, map(lambda file: os.path.join(path, file), files)))
#---        numFiles += len(files)
#---        usage[path] = sum(map(os.path.getsize, files))
#---    print("         {: <{}}".format("", width-9), end=backtrack)
#---    seconds = max(1, round(time.time() - started))
#---    dirRate = round(len(usage) / seconds, 1)
#---    fileRate = round(numFiles / seconds, 1)
#---    print("Found {} director{} with {} file{} in {} second{} ({} director{}/s, {} file{}/s)".format(
#---        format(len(usage), mode=Mode.grouped), "y" if len(usage) == 1 else "ies",
#---        format(numFiles, mode=Mode.grouped), "" if numFiles == 1 else "s",
#---        format(seconds, mode=Mode.grouped), "" if seconds == 1 else "s",
#---        format(dirRate, mode=Mode.grouped), "y" if dirRate == 1 else "ies",
#---        format(fileRate, mode=Mode.grouped), "" if fileRate == 1 else "s"))
#---    
#---    usage = sorted(usage.items(), key=lambda item:(-item[1], item[0]))
#---    widthCount = places(len(usage), min=2, mode=Mode.grouped)
#---    widthIndex = places(count, min=5-1-widthCount, mode=Mode.grouped)
#---    other = sum(map(lambda pair: pair[1], usage[count:]))
#---    total = sum(map(lambda pair: pair[1], usage))
#---    widthSize = max(
#---        max(map(lambda pair: places(pair[1], mode=MODE), usage[:count])),
#---        places(other, mode=MODE),
#---        places(total, mode=MODE))
#---    for i, (path, size) in enumerate(usage[:count]):
#---        print("{:>{}}/{} {:>{}} {}".format(format(i+1, mode=Mode.grouped), widthIndex, format(len(usage), mode=Mode.grouped), format(size, mode=MODE), widthSize, path))
#---    if (count < len(usage)):
#---        print("{:>{}} {:>{}}".format("Other", widthIndex+1+widthCount, format(other, mode=MODE), widthSize))
#---    print("{:>{}} {:>{}}".format("Total", widthIndex+1+widthCount, format(total, mode=MODE), widthSize))
    
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
