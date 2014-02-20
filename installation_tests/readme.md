DemandCube Developer Setup
====
- A [NeverwinterDP](https://github.com/DemandCube/NeverwinterDP) and [DemandCube](https://github.com/DemandCube) Project

Copywrite 2013 Steve Morin <steve@stevemorin.com>

Tests to ensure machines are set up correctly
====
Requires nosetests.  Uses Python to check binaries, file existence, and package versions


Prereqs
===
```
git clone git@github.com:DemandCube/developer-setup.git
cd developer-setup
./setup.sh
```

Running
===
```
cd ./installation_tests
mv -f ./test_configs/[config you wish to use].py ./config.py
#Need to run as sudo if you are checking running services
sudo nosetests -s
```
