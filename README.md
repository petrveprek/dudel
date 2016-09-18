# Welcome to *dudel*

__*dudel*__ -- **_du_**plicate **_del_**ete

# Usage

```
>dudel.py -h
Duplicate Delete 0.1
usage: dudel.py [-h] [-a {summary}]
                [-m {name,time,size} [{name,time,size} ...]]
                [-t {file,directory}] [-s] [-w <12,180>]
                [directory]

Finds and deletes duplicate files located under top `directory`.

positional arguments:
  directory             set top directory to clean up
                        [C:\Users\Admin\Documents\GitHub\dudel]

optional arguments:
  -h, --help            show this help message and exit
  -a {summary}, --action {summary}
                        set action to perform on found items [summary]
  -m {name,time,size} [{name,time,size} ...], --match {name,time,size} [{name,time,size} ...]
                        set criteria to detect duplicate items [['name',
                        'time', 'size']]
  -t {file,directory}, --type {file,directory}
                        set type of items to be searched for and deleted
                        [file]
  -s, --silent          suppress progress messages [false]
  -w <12,180>, --width <12,180>
                        set console width for progress indicator [180]
```

# Example

```
>dudel.py  \Windows
Duplicate Delete 0.1
Scanning files under \Windows
Found 26,081 directories with 131,563 files in 106 seconds (246.0 directories/s, 1,241.2 files/s)
Found 131,563 total items (34.3GiB), 94,345 unique items (21.9GiB), 37,218 duplicated items (12.5GiB), 27,858 groups with repeats, max 63 extra copies in a group
+-----------+------------+
| Directory | \Windows   |
+-----------+------------+
| Full path | C:\Windows |
+-----------+------------+
+-------------+---------+
|             |   Count |
+=============+=========+
| Directories |  26,081 |
+-------------+---------+
| Files       | 131,563 |
+-------------+---------+
```

Copyright (c) 2016 Petr Vepřek

MIT License, see [`LICENSE`](./LICENSE) for further details.
