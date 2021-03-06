#!python3
# Copyright (c) 2016 Petr Veprek
"""Duplicate Delete"""

import argparse, collections, colorama, datetime, enum, filecmp, os, string, sys, time, winshell

TITLE = "Duplicate Delete"
VERSION = "0.6"
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
    parser.add_argument("-a", "--action", choices=['summary', 'list', 'delete'], default='summary', help="set action to perform on found items [%(default)s]")
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
    types = {'sing.': "file", 'plur.': "files"} if type == 'file' else {'sing.': "directory", 'plur.': "directories"}
    
    if not silent:
        print("Scanning {} under {}".format(types['plur.'], directory))
        BACKTRACK = ("\r" if width < MAX_WIDTH else ANSI_CURSOR_UP) if sys.stdout.isatty() else "\n"
    started = time.time()
    numDirs, numFiles = (0,) * 2
    class Kind(enum.Enum): master = 0; copy = 1
    Item = collections.namedtuple('Item', ['location', 'name', 'time', 'size', 'group', 'kind'])
    items = []
    for path, dirs, files in os.walk(directory):
        if not silent:
            print("Scanning {: <{}}".format(printable(path[len(directory):] if path[len(directory):] != "" else "\\.", width-9), width-9), end=BACKTRACK)
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
        if sys.stdout.isatty():
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
        print("Sorting and grouping {}".format(types['plur.']))
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
        sizeUniqs = items[0].size
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
            items[1+index] = item._replace(group=0 if extra == 0 else numGroups, kind=Kind.master if extra == 0 else Kind.copy)
            prevItem = item
    assert numUniqs + numDups == len(items)
    if not silent:
        print("Found {} total {} ({}), {} unique {} ({}), {} duplicate {} ({}), {} group{} with repeats, max {} extra cop{} in a group".format(
            grouped(len(items)), types['sing.'  if len(items) == 1 else 'plur.'], gazillion(sizeUniqs+sizeDups),
            grouped(numUniqs),   types['sing.'  if numUniqs   == 1 else 'plur.'], gazillion(sizeUniqs),
            grouped(numDups),    types['sing.'  if numDups    == 1 else 'plur.'], gazillion(sizeDups),
            grouped(numGroups),  ""  if numGroups  == 1 else "s",
            grouped(maxExtra),   "y" if maxExtra   == 1 else "ies"))
    
    if 'contents' in match:
        if not silent:
            print("Matching {} contents".format(types['sing.']))
        begin = 0 # first item in pre-qualified group
        uniq = 1
        while begin < len(items):
            if not silent:
                print("Matching {: <{}}".format("{} of {}".format(grouped(uniq), grouped(numUniqs)), width-9), end=BACKTRACK)
            end = begin # last item in pre-qualified group
            while end < len(items)-1 and items[end+1].kind == Kind.copy:
                end += 1
            if begin < end:
                assert items[begin].kind == Kind.master
                assert items[end].kind == Kind.copy
                first = begin # first item in confirmed group
                while first <= end:
                    last = first # last item in confirmed group
                    while last <= end-1 and filecmp.cmp(
                        os.path.join(items[first].location, items[first].name),
                        os.path.join(items[last+1].location, items[last+1].name),
                        shallow=False):
                        last += 1
                    items[first] = items[first]._replace(kind=Kind.master)
                    for dup in range(first+1, last+1):
                        items[dup] = items[dup]._replace(kind=Kind.copy)
                    first = last + 1
            begin = end + 1
            uniq += 1
        if not silent:
            if sys.stdout.isatty():
                print("         {: <{}}".format("", width-9), end=BACKTRACK)
        numUniqs, numDups, numGroups, maxExtra, sizeUniqs, sizeDups = (0,) * 6
        for index, item in enumerate(items):
            if item.kind == Kind.master:
                numUniqs += 1
                sizeUniqs += item.size
                extra = 0
                items[index] = item._replace(group=0)
            else:
                assert item.kind == Kind.copy
                numDups +=1
                sizeDups += item.size
                if extra == 0:
                    numGroups += 1
                extra += 1
                maxExtra = max(extra, maxExtra)
                items[index] = item._replace(group=numGroups)
        assert numUniqs + numDups == len(items)
        if not silent:
            print("Found {} total {} ({}), {} unique {} ({}), {} duplicate {} ({}), {} group{} with repeats, max {} extra cop{} in a group".format(
                grouped(len(items)), types['sing.'  if len(items) == 1 else 'plur.'], gazillion(sizeUniqs+sizeDups),
                grouped(numUniqs),   types['sing.'  if numUniqs   == 1 else 'plur.'], gazillion(sizeUniqs),
                grouped(numDups),    types['sing.'  if numDups    == 1 else 'plur.'], gazillion(sizeDups),
                grouped(numGroups),  ""  if numGroups  == 1 else "s",
                grouped(maxExtra),   "y" if maxExtra   == 1 else "ies"))
    
    if action in ['summary', 'list', 'delete']:
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
            ["Duplicate",                                  grouped(numDups),           gazillion(sizeDups),           "{:.1%}".format(sizeDups/(sizeUniqs+sizeDups) if sizeUniqs+sizeDups != 0 else 0)],
            ["Groups",                                     grouped(numGroups),         "-",                           "-"],
            ["Max extra",                                  grouped(maxExtra),          "-",                           "-"]],
            numHeaderRows = 1,
            columnAlign = ['left'] + ['right'] * 3,
            rowSeparator = [True] * 6),
            end="")
        Location = collections.namedtuple('Location', ['masters', 'copies'])
        location = {}
        for item in items:
            if item.kind == Kind.copy:
                if prevItem.kind == Kind.master:
                    assert prevItem.group == 0
                    if prevItem.location not in location.keys():
                        location[prevItem.location] = Location(masters=0, copies=0)
                    location[prevItem.location] = location[prevItem.location]._replace(masters=location[prevItem.location].masters+1)
                if item.location not in location.keys():
                    location[item.location] = Location(masters=0, copies=0)
                location[item.location] = location[item.location]._replace(copies=location[item.location].copies+1)
            prevItem = item
        data = [["Location", "Master count", "Copy count"]]
        for path in sorted(location.keys(), key=lambda path: (-location[path].masters, -location[path].copies, path)):
            data.append([printable(path), grouped(location[path].masters), grouped(location[path].copies)])
        print(tabulated(data,
            numHeaderRows = 1,
            columnAlign = ['left'] + ['right'] * 2,
            rowSeparator = [True]),
            end="")
    if action in ['list', 'delete']:
        data = [["Group", "Name", "Location", "Time", "Size"]]
        groupEnd = [True]
        for item in items:
            if item.kind == Kind.copy:
                if prevItem.kind == Kind.master:
                    assert prevItem.group == 0
                    groupEnd[-1] = True
                    data.append(["Master", printable(prevItem.name), printable(prevItem.location), timestamp(prevItem.time), gazillion(prevItem.size)])
                    groupEnd.append(False)
                    if action == 'delete':
                        masterName     = prevItem.name
                        masterLocation = prevItem.location
                        master = os.path.join(masterLocation, masterName)
                data.append([grouped(item.group), printable(item.name), printable(item.location), timestamp(item.time), gazillion(item.size)])
                groupEnd.append(False)
                if action == 'delete':
                    copyName     = item.name
                    copyLocation = item.location
                    copy = os.path.join(copyLocation, copyName)
                    link = copy + '.link'
                    try:
                        with open(link, 'w') as link:
                            link.write(master) # Precaution #1: Create a link to the master.
                    except:
                        try:
                            print('Failed to create link to master')
                        except:
                            pass
                    else:
                        winshell.delete_file(copy, no_confirm=True) # Precaution #2: Move copy to the recycle bin.
                        try:
                            print('Deleted "', copy, '"')
                        except:
                            pass
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

#  [?] to list, add md5/sha/crc  [!] if not silent report rematch result  [1] match contents  [2] color  [3] pick=shallow...  [4] action=rename  [5] graphic border
# add confirm for deletions
# add count >MAX_PATH (260)
# do group match: all at once? (current one-to-next may miss dups and require multiple passes)
# master pick/selection: alpha/shortest/shallowest-path
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
