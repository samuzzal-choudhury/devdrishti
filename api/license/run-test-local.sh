#! /bin/bash


export TERM=xterm
TERM=${TERM:-xterm}

# set up terminal colors
NORMAL=$(tput sgr0)
RED=$(tput bold && tput setaf 1)
GREEN=$(tput bold && tput setaf 2)
YELLOW=$(tput bold && tput setaf 3)

# Usage info
# Ref. Link http://mywiki.wooledge.org/BashFAQ/035
show_help() {
cat << EOF
Usage: ${0##*/} [-h] [-t MAJORITY_THRESHOLD]
Run the unit test in your local environment.

    -h display this help and exit
    -t MAJORITY_THRESHOLD Set the outlier threshold value
EOF
}

#Set default values
threshold=0.6

while getopts ht: opt; do
# t is an optional argument, but requires a value when present in the command line.

  case $opt in
    h)
      show_help
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    t) threshold=$OPTARG
      ;;
  esac
done

export MAJORITY_THRESHOLD=$threshold
export DATA_DIR=.

PYTHONPATH=$(pwd)/src
export PYTHONPATH

printf "%sCreate Virtualenv for Python deps ..." "${NORMAL}"

function prepare_venv() {
    virtualenv -p python3 venv && source venv/bin/activate && python3 "$(which pip3)" install -r requirements.txt
    if [ $? -ne 0 ]
    then
        printf "%sPython virtual environment can't be initialized%s" "${RED}" "${NORMAL}"
        exit 1
    fi
    printf "%sPython virtual environment initialized%s\n" "${YELLOW}" "${NORMAL}"
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

export DISABLE_AUTHENTICATION=1

# the module src/config.py must exists because it is included from stack_license and license_analysis.py as well.
cp src/config.py.template src/config.py
cd tests || exit
mkdir testdir1
mkdir testdir4
PYTHONDONTWRITEBYTECODE=1 python3 "$(which pytest)" --cov=../src/ --cov-report term-missing -vv -s .
rm -rf testdir1
rm -rf testdir4
printf "%stests passed%s\n\n" "${GREEN}" "${NORMAL}"
