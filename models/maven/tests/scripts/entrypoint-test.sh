#!/usr/bin/env bash

check_python_version() {
    python3 /tools/check_python_version.py 3 6
}

locale charmap

check_python_version

export RADONFILESENCODING=UTF-8

echo "*****************************************"
echo "*** Cyclomatic complexity measurement ***"
echo "*****************************************"
radon cc -s -a -i usr .

echo "*****************************************"
echo "*** Maintainability Index measurement ***"
echo "*****************************************"
radon mi -s -i usr .

echo "*****************************************"
echo "*** Unit tests ***"
echo "*****************************************"

mkdir /tmp/hpf # Need to create this dir as shutil.copyfile does not create parents
PYTHONHASHSEED=1 pytest --cov=/src/ --cov-report term-missing -vv /tests/unit_tests/

codecov --token=773b7a11-8e23-4244-9047-ed3c02ff33f0
