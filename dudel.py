#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""

import argparse, collections, colorama, datetime, enum, os, string, sys, time

TITLE = "Duplicate Delete"
VERSION = "0.3"
VERBOSE = False
class Mode(enum.Enum): plain = 0; grouped = 1; gazillion = 2
MIN_WIDTH = 9+0+3 # intro + directory + ellipsis
MAX_WIDTH = os.get_terminal_size().columns if sys.stdout.isatty() else 80
WIDTH = MAX_WIDTH
WIDTH = min(max(WIDTH, MIN_WIDTH), MAX_WIDTH)
ANSI_CURSOR_UP = "\033[A"

def now(on="on", at="at"):
    return "{}{} {}{}".format(
        on + " " if on != "" else "", time.strftime("%Y-%m-%d"),
        at + " " if at != "" else "", time.strftime("%H:%M:%S"))

def printable(str, max=None):
    str = "".join([char if char in string.printable else "?" for char in str])
    if max != None and len(str) > max: str = str[:max-3] + "..."
    return str

def plain(num):
    return "{}".format(num)

def grouped(num):
    return "{:,}".format(num)

def gazillion(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if num < 1024.0:
            return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, unit, suffix)
        num /= 1024.0
    return "{:.{}f}{}{}".format(num, 1 if num % 1 > 0 else 0, "Yi", suffix)

def format(num, mode=Mode.plain):
    return(
        grouped(num)   if mode == Mode.grouped   else
        gazillion(num) if mode == Mode.gazillion else
        plain(num))

def timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")

def tabulated(table, numHeaderRows=0, columnAlign=[], rowSeparator=[]):
    numRows = len(table)
    numCols = len(table[0])
    colWidths = [max(len(table[row][col]) for row in range(numRows)) for col in range(numCols)]
    headerSep = "+" + "".join("={:=<{}}=+".format("", colWidths[col]) for col in range(numCols)) + "\n"
    rowSep = "".join([char if char != "=" else "-" for char in headerSep])
    headerFmt = "|" + "".join(" {: " + ((
        "<" if columnAlign[col] == 'left' else
        ">" if columnAlign[col] == 'right' else
        "^") if col < len(columnAlign) else "^") +
        str(colWidths[col]) + "} |" for col in range(numCols)) + "\n"
    rowFmt = "".join([char if char != "^" else "<" for char in headerFmt])
    return rowSep + "".join(
        (headerFmt if row < numHeaderRows else rowFmt).format(*table[row]) + \
        ((headerSep if row < numHeaderRows else rowSep) if row == numRows-1 or row < len(rowSeparator) and rowSeparator[row] else "") +
        (rowSep if numHeaderRows == numRows else "") \
        for row in range(numRows))

def main():
    colorama.init()
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
    parser.add_argument("-a", "--action", choices=['summary', 'list'], default='summary', help="set action to perform on found items [%(default)s]")
    parser.add_argument("-m", "--match", nargs="+", choices=['name', 'time', 'size', 'contents'], default=['name', 'time', 'size', 'contents'], help="set criteria to detect duplicate items ["+" ".join(['name', 'time', 'size', 'contents'])+"]")
    parser.add_argument("-t", "--type", choices=['file', 'directory'], default='file', help="set type of items to be searched for and deleted [%(default)s]")
    parser.add_argument("-s", "--silent", action="store_true", default=False, help="suppress progress messages [false]")
    parser.add_argument("-w", "--width", type=int, choices=range(MIN_WIDTH,MAX_WIDTH+1), default=WIDTH, metavar="<{},{}>".format(MIN_WIDTH,MAX_WIDTH), help="set console width for progress indicator [%(default)s]")
    arguments = parser.parse_args()
    directory = arguments.directory
    action = arguments.action
    match = arguments.match
    type = arguments.type
    silent = arguments.silent
    width = arguments.width
    
    if not silent:
        print("Scanning {} under {}".format("files" if type == 'file' else "directories", directory))
        BACKTRACK = ("\r" if width < MAX_WIDTH else ANSI_CURSOR_UP) if sys.stdout.isatty() else "\n"
    started = time.time()
    numDirs, numFiles = (0,) * 2
    class Kind(enum.Enum): master = 0; copy = 1
    Item = collections.namedtuple('Item', ['location', 'name', 'time', 'size', 'group', 'kind'])
    items = []
    for path, dirs, files in os.walk(directory):
        if not silent:
            print("Scanning {: <{}}".format(printable(path[len(directory):], width-9), width-9), end=BACKTRACK)
        dirs  = list(filter(os.path.isdir,  map(lambda dir:  os.path.abspath(os.path.join(path, dir)),  dirs)))
        files = list(filter(os.path.isfile, map(lambda file: os.path.abspath(os.path.join(path, file)), files)))
        numDirs  += len(dirs)
        numFiles += len(files)
        for element in files if type == 'file' else dirs:
            location, name = os.path.split(element)
            mtime = os.path.getmtime(element)
            size = os.path.getsize(element)
            items.append(Item(location=location, name=name, time=mtime, size=size, group=None, kind=None))
    if not silent:
        print("         {: <{}}".format("", width-9), end=BACKTRACK)
        seconds = max(1, round(time.time() - started))
        dirRate  = round(numDirs  / seconds, 1)
        fileRate = round(numFiles / seconds, 1)
        print("Found {} director{} with {} file{} in {} second{} ({} director{}/s, {} file{}/s)".format(
            grouped(numDirs),  "y" if numDirs  == 1 else "ies",
            grouped(numFiles), ""  if numFiles == 1 else "s",
            grouped(seconds),  ""  if seconds  == 1 else "s",
            grouped(dirRate),  "y" if dirRate  == 1 else "ies",
            grouped(fileRate), ""  if fileRate == 1 else "s"))
    
    if not silent:
        print("Sorting and grouping items")
    items.sort(key=lambda item:
        ((item.name,) if 'name' in match else ()) +
        ((item.time,) if 'time' in match else ()) +
        ((item.size,) if 'size' in match else ()) +
        ((item.name,) if 'name' not in match else ()) +
        ((item.time,) if 'time' not in match else ()) +
        ((item.size,) if 'size' not in match else ()) +
        ((item.location,)))
    numUniqs, numDups, numGroups, maxExtra, sizeUniqs, sizeDups = (0,) * 6
    if len(items) > 0:
        numUniqs = 1
        extra = 0
        items[0] = items[0]._replace(group=0, kind=Kind.master)
        prevItem = items[0]
        for index, item in enumerate(items[1:]):
            if ('name' not in match or item.name == prevItem.name) and \
               ('time' not in match or item.time == prevItem.time) and \
               ('size' not in match or item.size == prevItem.size):
                numDups += 1
                if extra == 0:
                    numGroups += 1
                extra += 1
                maxExtra = max(extra, maxExtra)
                sizeDups += item.size
            else:
                numUniqs += 1
                extra = 0
                sizeUniqs += item.size
            items[index] = item._replace(group=0 if extra == 0 else numGroups, kind=Kind.master if extra == 0 else Kind.copy)
            prevItem = item
    assert numUniqs + numDups == len(items)
    if not silent:
        print("Found {} total item{} ({}), {} unique item{} ({}), {} duplicated item{} ({}), {} group{} with repeats, max {} extra cop{} in a group".format(
            grouped(len(items)), ""  if len(items) == 1 else "s", gazillion(sizeUniqs+sizeDups),
            grouped(numUniqs),   ""  if numUniqs   == 1 else "s", gazillion(sizeUniqs),
            grouped(numDups),    ""  if numDups    == 1 else "s", gazillion(sizeDups),
            grouped(numGroups),  ""  if numGroups  == 1 else "s",
            grouped(maxExtra),   "y" if maxExtra   == 1 else "ies"))
    
    if action in ['summary', 'list']:
        print(tabulated([
            ["Directory", directory],
            ["Full path", os.path.abspath(directory)]],
            rowSeparator = [True] * 2),
            end="")
        print(tabulated([
            ["",            "Count"],
            ["Directories", grouped(numDirs)],
            ["Files",       grouped(numFiles)]],
            numHeaderRows = 1,
            columnAlign = ['left'] + ['right'] * 1,
            rowSeparator = [True] * 3),
            end="")
        print(tabulated([
            ["Files" if type == "file" else "Directories", "Count",                    "Size",                        "Percent"],
            ["Total",                                      grouped(numUniqs+numDups),  gazillion(sizeUniqs+sizeDups), "100.0%"],
            ["Unique",                                     grouped(numUniqs),          gazillion(sizeUniqs),          "{:.1%}".format(sizeUniqs/(sizeUniqs+sizeDups) if sizeUniqs+sizeDups != 0 else 0)],
            ["Duplicated",                                 grouped(numDups),           gazillion(sizeDups),           "{:.1%}".format(sizeDups/(sizeUniqs+sizeDups) if sizeUniqs+sizeDups != 0 else 0)],
            ["Groups",                                     grouped(numGroups),         "-",                           "-"],
            ["Max extra",                                  grouped(maxExtra),          "-",                           "-"]],
            numHeaderRows = 1,
            columnAlign = ['left'] + ['right'] * 3,
            rowSeparator = [True] * 6),
            end="")
    if action == 'list':
        data = [["Group", "Name", "Location", "Time", "Size"]]
        groupEnd = [True]
        for item in items:
            if item.kind == Kind.copy:
                if prevItem.kind == Kind.master:
                    groupEnd[-1] = True
                    data.append(["Master", printable(prevItem.name), printable(prevItem.location), timestamp(prevItem.time), gazillion(prevItem.size)])
                    groupEnd.append(False)
                data.append([grouped(item.group), printable(item.name), printable(item.location), timestamp(item.time), gazillion(item.size)])
                groupEnd.append(False)
            prevItem = item
        groupEnd[-1] = True
        print(tabulated(data,
            numHeaderRows = 1,
            columnAlign = ['right'] + ['left'] * 2 + ['right'] * 2,
            rowSeparator = groupEnd),
            end="")
    
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

# [1] match content  [2] color  [3] pick=shallow...  [4] action=rename
# master pick/selection: alpha/shortest/shallowest-path
# dius printable _ -> ?
# printable: return string.encode(sys.stdout.encoding, errors='replace')
# dudel master inspect (when several file copies exist, keep the ones (even multiple) in master directory, delete all from inspect directory)
# --find unique/duplicate(multiple)
# --match /extension///sha1-crc32-md5/content(byte-by-byte)
# --action scan~~list(show)/delete/move/rename
# --mode
#? keep MASTER reference original prototype source exemplar
#? prune check search COPY target
#? match sub-tree / file name / extension / date-time / size / content
#? sh1 / md5 ... byte-by-byte (identical)
#? interactive mode
#? find unique|dup files|directories
#? do not delete, show only | move to | rename
#? action: summary/list/show, delete, rename?, move?
#? sys.stdout.isatty() --> if not, then no progress or no backtrack
#? no progress, silent
#? a] master
#? b] master copy
#? force
# prune / sort / save md5 et al / keep empty dirs / STATS
