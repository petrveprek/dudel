#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""

import argparse, collections, enum, os, string, sys, time

TITLE = "Duplicate Delete"
VERSION = "0.1"
VERBOSE = False
class Mode(enum.Enum): plain = 0; grouped = 1; gazillion = 2
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

def plain(num):
    return "{}".format(num)

def grouped(num):
    return "{:,}".format(num)

def gazillion(num, suffix="B"):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if num < 1024.0:
            return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, unit, suffix)
        num /= 1024.0
    return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, 'Yi', suffix)

def format(num, mode=Mode.plain):
    return(
        grouped(num)   if mode == Mode.grouped   else
        gazillion(num) if mode == Mode.gazillion else
        plain(num))

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
    parser.add_argument("directory", nargs="?", default=os.getcwd(), help="set top directory to clean up [%(default)s]")
    parser.add_argument("-t", "--type", choices=["file", "directory"], default="file", help="set type of items to be searched for and deleted [%(default)s]")
    parser.add_argument("-m", "--match", nargs="+", choices=["name", "time", "size"], default="name time size", help="set criteria to detect duplicate items [%(default)s]")
    parser.add_argument("-w", "--width", type=int, choices=range(MIN_WIDTH,MAX_WIDTH+1), default=WIDTH, metavar="<{},{}>".format(MIN_WIDTH,MAX_WIDTH), help="set console width for progress indicator [%(default)s]")
    parser.add_argument("-s", "--silent", action="store_true", default=False, help="suppress progress messages [false]")
    arguments = parser.parse_args()
    directory = arguments.directory
    type = arguments.type
    match = arguments.match
    width = arguments.width
    silent = arguments.silent
    
    if not silent:
        print("Scanning {} under {}".format("files" if type == "file" else "directories", directory))
        BACKTRACK = ("\r" if width < MAX_WIDTH else "\033[F") if sys.stdout.isatty() else "\n"
    started = time.time()
    numDirs, numFiles = (0,) * 2
    Item = collections.namedtuple('Item', ['name', 'location', 'time', 'size'])
    items = []
    for path, dirs, files in os.walk(directory):
        if not silent:
            print("Scanning {: <{}}".format(printable(path, width-9), width-9), end=BACKTRACK)
        dirs  = list(filter(os.path.isdir,  map(lambda dir:  os.path.abspath(os.path.join(path, dir)),  dirs)))
        files = list(filter(os.path.isfile, map(lambda file: os.path.abspath(os.path.join(path, file)), files)))
        numDirs  += len(dirs)
        numFiles += len(files)
        for element in files if type == "file" else dirs:
            location, name = os.path.split(element)
            time_ = os.path.getmtime(element)
            size = os.path.getsize(element)
            items.append(Item(name=name, location=location, time=time_, size=size))
    if not silent:
        print("         {: <{}}".format("", width-9), end=BACKTRACK)
        seconds = max(1, round(time.time() - started))
        dirRate  = round(numDirs  / seconds, 1)
        fileRate = round(numFiles / seconds, 1)
        print("Found {} director{} with {} file{} in {} second{} ({} director{}/s, {} file{}/s)".format(
            format(numDirs,  mode=Mode.grouped), "y" if numDirs  == 1 else "ies",
            format(numFiles, mode=Mode.grouped), ""  if numFiles == 1 else "s",
            format(seconds,  mode=Mode.grouped), ""  if seconds  == 1 else "s",
            format(dirRate,  mode=Mode.grouped), "y" if dirRate  == 1 else "ies",
            format(fileRate, mode=Mode.grouped), ""  if fileRate == 1 else "s"))
    
    items.sort(key=lambda item:(item.name, item.location))
    numUniq, maxExtra = (0,) * 2
    if len(items) > 0:
        numUniq = 1
        prevItem = items[0]
        extra = 0
        for item in items[1:]:
#            print(item)
            if ("name" not in match or item.name == prevItem.name) and \
               ("time" not in match or True) and \
               ("size" not in match or True):
                extra += 1
                maxExtra = max(extra, maxExtra)
            else:
                numUniq += 1
                extra = 0
            prevItem = item
    print("Found {} total item{}, {} unique item{}, {} max extra copies".format(
        len(items), "" if len(items) == 1 else "s",
        numUniq,    "" if numUniq    == 1 else "s",
        maxExtra,   "" if maxExtra   == 1 else "s"))
    
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

# printable: return string.encode(sys.stdout.encoding, errors='replace')
# dudel master inspect (when several file copies exist, keep the ones (even multiple) in master directory, delete all from inspect directory)
# --find unique/duplicate(multiple)
# --match /extension///sha1-crc32-md5/content(byte-by-byte)
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
