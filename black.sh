#! /bin/bash
if [ $# -eq 0 ]; then
  FILES=$(find . -name '*.py') 
else
  FILES=$*
fi
black -l 80 -t py38 $FILES
exit $?
