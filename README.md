# Welcome to *dudel*

__*dudel*__ -- **_du_**plicate **_del_**ete

# Usage

```
>dudel.py -h
Duplicate Delete 0.1
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
Duplicate Delete 0.1
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
+--------+------------+-------------------------------------------------+
|  Group | Name       | Location                                        |
+========+============+=================================================+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0011 |
|      1 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0012 |
|      1 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0013 |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0014 |
|      2 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0021 |
|      2 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0024 |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0005 |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0006 |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0009 |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001a |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001d |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\002d |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0404 |
|      3 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0804 |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0007 |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0019 |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001b |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0416 |
|      4 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0816 |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0003 |
|      5 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0008 |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\000b |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001f |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\040c |
|      6 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\0c0c |
+--------+------------+-------------------------------------------------+
| Master | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\000e |
|      7 | _setup.dll | C:\Windows\SysWOW64\InstallShield\setupdir\001e |
+--------+------------+-------------------------------------------------+
```

Copyright (c) 2016 Petr Vepřek

MIT License, see [`LICENSE`](./LICENSE) for further details.
