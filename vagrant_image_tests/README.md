QA-NeverwinterDP
====
- A [NeverwinterDP](https://github.com/DemandCube/NeverwinterDP) and [DemandCube](https://github.com/DemandCube) Project

Copywrite 2013 Steve Morin <steve@stevemorin.com>

Tests to ensure vagrant images are set up correctly
====
Requires nosetests. (https://nose.readthedocs.org/en/latest/)

Uses nose/python to check binaries, file existence, and package versions


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
Edit config.py file to set the name and URL/path of the vagrant box you want test and do
```
$ cd ./vagrant_image_tests
$ nosetests
```
