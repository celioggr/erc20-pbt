#! /bin/bash

export PYTHONPATH=$(dirname $0)

usage() {
  echo "Usage:"
  echo "  $(basename $0) [options] test1 ... testn"
  echo "Options:"
  echo "  -c <arg> : set stateful step count"
  echo "  -n <arg> : set maximum examples"
  echo "  -s <arg> : set seed for tests"
  echo "  -C       : measure coverage"
  echo "  -D       : enable debug output"
  echo "  -E       : enable verification of events"
  echo "  -R       : enable verification of return values"
  echo "  -S       : enable shrinking"
}

PBT_DEBUG=no
PBT_SEED=0
PBT_MAX_EXAMPLES=100
PBT_STATEFUL_STEP_COUNT=10
PBT_PROFILE=generate
PBT_VERIFY_EVENTS=no
PBT_VERIFY_RETURN_VALUES=no
coverage_setting=''

while getopts ":c:n:s:CDERS" options; do
  case "${options}" in  
    c)
      PBT_STATEFUL_STEP_COUNT=${OPTARG}
      ;;
    n) 
      PBT_MAX_EXAMPLES=${OPTARG}
      ;;
    s)
      PBT_SEED=${OPTARG}
      ;;
    C)
      coverage_setting="--coverage"
      ;;
    D)
      PBT_DEBUG=yes
      ;;
    E)
      PBT_VERIFY_EVENTS=yes
      ;;
    R)
      PBT_VERIFY_RETURN_VALUES=yes
      ;;
    S) 
      PBT_PROFILE="shrinking"
      ;;
    :)
      echo "Error: -${OPTARG} requires an argument."
      usage
      exit 1
      ;;

    *)
      echo Invalid arguments!
      usage
      exit 1
      ;;
  esac
done

shift $(expr $OPTIND - 1 )

if [ "$#" -eq 0 ]; then
  echo No tests specified for execution!
  usage
  exit 1
fi
echo --- Environment 
export PBT_SEED PBT_MAX_EXAMPLES PBT_STATEFUL_STEP_COUNT PBT_PROFILE PBT_VERIFY_EVENTS PBT_VERIFY_RETURN_VALUES PBT_DEBUG
env | grep ^PBT

extra_args=''

if [ "$PBT_DEBUG" == "yes" ]; then
  extra_args="-s"
fi

echo --- Running tests
pytest --hypothesis-profile=$PBT_PROFILE $* $extra_args $coverage_setting
