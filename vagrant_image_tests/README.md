DemandCube Developer Setup
====
- A [NeverwinterDP](https://github.com/DemandCube/NeverwinterDP) and [DemandCube](https://github.com/DemandCube) Project

Copywrite 2013 Steve Morin <steve@stevemorin.com>

Tests to ensure machines are set up correctly
====
Requires nosetests. (https://nose.readthedocs.org/en/latest/)

Uses nose/Python to check binaries, file existence, and package versions


Prerequisites
===
```
1. virtualbox
2. vagrant
3. nosetests

For this
$ git clone git@github.com:DemandCube/developer-setup.git
$ cd developer-setup
$ ./setup.sh
```

Running
===
```
cd ./vagrant_image_tests
$nosetests
```
