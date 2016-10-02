# Welcome to *dudel*

__*dudel*__ -- **_du_**plicate **_del_**ete

# Usage

```
>dudel.py -h
Duplicate Delete 0.2
usage: dudel.py [-h] [-a {summary,list}]
                [-m {name,time,size} [{name,time,size} ...]]
                [-t {file,directory}] [-s] [-w <12,180>]
                [directory]

Finds and deletes duplicate files located under top `directory`.

positional arguments:
  directory             set top directory to clean up
                        [C:\Users\Admin\Documents\GitHub\dudel]

optional arguments:
  -h, --help            show this help message and exit
  -a {summary,list}, --action {summary,list}
                        set action to perform on found items [summary]
  -m {name,time,size} [{name,time,size} ...], --match {name,time,size} [{name,time,size} ...]
                        set criteria to detect duplicate items [name time
                        size]
  -t {file,directory}, --type {file,directory}
                        set type of items to be searched for and deleted
                        [file]
  -s, --silent          suppress progress messages [false]
  -w <12,180>, --width <12,180>
                        set console width for progress indicator [180]
```

# Example

```
>dudel.py \Windows\SysWOW64\InstallShield -s -a list
Duplicate Delete 0.2
+-----------+-----------------------------------+
| Directory | \Windows\SysWOW64\InstallShield   |
+-----------+-----------------------------------+
| Full path | C:\Windows\SysWOW64\InstallShield |
+-----------+-----------------------------------+
+-------------+-------+
|             | Count |
+=============+=======+
| Directories |    31 |
+-------------+-------+
| Files       |    33 |
+-------------+-------+
+------------+-------+----------+---------+
| Files      | Count |     Size | Percent |
+============+=======+==========+=========+
| Total      |    33 |   1.1MiB |  100.0% |
+------------+-------+----------+---------+
| Unique     |    13 | 448.5KiB |   39.6% |
+------------+-------+----------+---------+
| Duplicated |    20 | 684.5KiB |   60.4% |
+------------+-------+----------+---------+
| Groups     |     7 |        - |       - |
+------------+-------+----------+---------+
| Max extra  |     7 |        - |       - |
+------------+-------+----------+---------+
+--------+------------+-------------------------------------------------+----------------------------+---------+
|  Group | Name       | Location                                        |                       Time |    Size |
+========+============+=================================================+============================+=========+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0011 | 2016-07-16 12:42:45.436913 |   34KiB |
|      1 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0012 | 2016-07-16 12:42:45.436913 |   34KiB |
|      1 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0013 | 2016-07-16 12:42:45.436913 |   34KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0014 | 2016-07-16 12:42:45.436913 | 34.5KiB |
|      2 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0021 | 2016-07-16 12:42:45.436913 | 34.5KiB |
|      2 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0024 | 2016-07-16 12:42:45.436913 | 34.5KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0005 | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0006 | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0009 | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001a | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001d | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\002d | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0404 | 2016-07-16 12:42:46.405661 |   34KiB |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0804 | 2016-07-16 12:42:46.405661 |   34KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0007 | 2016-07-16 12:42:46.405661 | 34.5KiB |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0019 | 2016-07-16 12:42:46.405661 | 34.5KiB |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001b | 2016-07-16 12:42:46.405661 | 34.5KiB |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0416 | 2016-07-16 12:42:46.405661 | 34.5KiB |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0816 | 2016-07-16 12:42:46.405661 | 34.5KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0003 | 2016-07-16 12:42:46.405661 |   35KiB |
|      5 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0008 | 2016-07-16 12:42:46.405661 |   35KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\000b | 2016-07-16 12:42:46.421286 |   34KiB |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001f | 2016-07-16 12:42:46.421286 |   34KiB |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\040c | 2016-07-16 12:42:46.421286 |   34KiB |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0c0c | 2016-07-16 12:42:46.421286 |   34KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\000e | 2016-07-16 12:42:46.421286 | 34.5KiB |
|      7 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001e | 2016-07-16 12:42:46.421286 | 34.5KiB |
+--------+------------+-------------------------------------------------+----------------------------+---------+
```

Copyright (c) 2016 Petr Vepřek

MIT License, see [`LICENSE`](./LICENSE) for further details.
