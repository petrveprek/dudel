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
>dudel.py \Windows
Duplicate Delete 0.1
Scanning files under \Windows
Found 23,184 directories with 115,027 files in 48 seconds (483.0 directories/s, 2,396.4 files/s)
Found 115,027 total items (50.2GiB), 78,732 unique items (23.2GiB), 36,295 duplicated items (27.0GiB), 26,883 groups with repeats, max 63 extra copies in a group
+-----------+------------+
| Directory | \Windows   |
+-----------+------------+
| Full path | C:\Windows |
+-----------+------------+
+-------------+---------+
|             |   Count |
+=============+=========+
| Directories |  23,184 |
+-------------+---------+
| Files       | 115,027 |
+-------------+---------+
+------------+---------+---------+---------+
| Files      |   Count |    Size | Percent |
+============+=========+=========+=========+
| Total      | 115,027 | 50.2GiB |  100.0% |
+------------+---------+---------+---------+
| Unique     |  78,732 | 23.2GiB |   46.2% |
+------------+---------+---------+---------+
| Duplicated |  36,295 | 27.0GiB |   53.8% |
+------------+---------+---------+---------+
| Groups     |  26,883 |       - |       - |
+------------+---------+---------+---------+
| Max extra  |      63 |       - |       - |
+------------+---------+---------+---------+
```

Copyright (c) 2016 Petr Vepřek

MIT License, see [`LICENSE`](./LICENSE) for further details.
