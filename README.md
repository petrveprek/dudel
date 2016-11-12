# Welcome to *dudel*

__*dudel*__ -- **_du_**plicate **_del_**ete

# Usage

```
>dudel.py -h
Duplicate Delete 0.6
usage: dudel.py [-h] [-a {summary,list,delete}]
                [-m {name,time,size,contents} [{name,time,size,contents} ...]]
                [-t {file,directory}] [-s] [-w <12,180>]
                [directory]

Finds and deletes duplicate files located under top `directory`.

positional arguments:
  directory             set top directory to clean up
                        [C:\Users\Admin\Documents\GitHub\dudel]

optional arguments:
  -h, --help            show this help message and exit
  -a {summary,list,delete}, --action {summary,list,delete}
                        set action to perform on found items [summary]
  -m {name,time,size,contents} [{name,time,size,contents} ...], --match {name,time,size,contents} [{name,time,size,contents} ...]
                        set criteria to detect duplicate items [name time size
                        contents]
  -t {file,directory}, --type {file,directory}
                        set type of items to be searched for and deleted
                        [file]
  -s, --silent          suppress progress messages [false]
  -w <12,180>, --width <12,180>
                        set console width for progress indicator [180]
```

# Example

```
>dudel.py \Windows\SysWOW64 -a list
Duplicate Delete 0.6
Scanning files under \Windows\SysWOW64
Found 350 directories with 5,644 files in 2 seconds (175.0 directories/s, 2,822.0 files/s)
Sorting and grouping files
Found 5,644 total files (1.4GiB), 5,511 unique files (1.4GiB), 133 duplicate files (2.9MiB), 67 groups with repeats, max 7 extra copies in a group
Matching file contents
Found 5,644 total files (1.4GiB), 5,643 unique files (1.4GiB), 1 duplicate file (35.9KiB), 1 group with repeats, max 1 extra copy in a group
+-----------+---------------------+
| Directory | \Windows\SysWOW64   |
+-----------+---------------------+
| Full path | C:\Windows\SysWOW64 |
+-----------+---------------------+
+-------------+-------+
|             | Count |
+=============+=======+
| Directories |   350 |
+-------------+-------+
| Files       | 5,644 |
+-------------+-------+
+-----------+-------+---------+---------+
| Files     | Count |    Size | Percent |
+===========+=======+=========+=========+
| Total     | 5,644 |  1.4GiB |  100.0% |
+-----------+-------+---------+---------+
| Unique    | 5,643 |  1.4GiB |  100.0% |
+-----------+-------+---------+---------+
| Duplicate |     1 | 35.9KiB |    0.0% |
+-----------+-------+---------+---------+
| Groups    |     1 |       - |       - |
+-----------+-------+---------+---------+
| Max extra |     1 |       - |       - |
+-----------+-------+---------+---------+
+--------------------------------------------------+--------------+------------+
| Location                                         | Master count | Copy count |
+==================================================+==============+============+
| C:\Windows\SysWOW64                              |            1 |          0 |
| C:\Windows\SysWOW64\en-US\Licenses\_Default\Core |            0 |          1 |
+--------------------------------------------------+--------------+------------+
+--------+-------------+--------------------------------------------------+----------------------------+---------+
|  Group | Name        | Location                                         |                       Time |    Size |
+========+=============+==================================================+============================+=========+
| Master | license.rtf | C:\Windows\SysWOW64                              | 2016-07-16 15:12:49.070815 | 35.9KiB |
|      1 | license.rtf | C:\Windows\SysWOW64\en-US\Licenses\_Default\Core | 2016-07-16 15:12:49.070815 | 35.9KiB |
+--------+-------------+--------------------------------------------------+----------------------------+---------+
```

# Warning

**Achtung! Action `delete` may result in files being DELETED.** It is highly recommended to first use `list` action  and
review the list of found duplicate items.

Copyright (c) 2016 Petr Vepřek

MIT License, see [`LICENSE`](./LICENSE) for further details.
