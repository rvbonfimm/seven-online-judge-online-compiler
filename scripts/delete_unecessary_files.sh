#!/bin/bash

#
#
# Search for all files with extensions .pyc, .c, .judgelog for cleaning
#
#

cfiles_qtt=0
pycfiles_qtt=0
judgelogfiles_qtt=0

# Selecting all .c files
cfiles=`find /home/eliseuvidaloca/Desktop/development/sevenonlinejudge/compiler | egrep "\.c$"`

for file in $cfiles
do
    let "cfiles_qtt+=1"
    rm -v $file
done

# Selecting all .pyc files
pycfiles=`find /home/eliseuvidaloca/Desktop/development/sevenonlinejudge | egrep "\.pyc$"`

for file in $pycfiles
do
    let "pycfiles_qtt+=1"
    rm -v $file
done

# Selecting all .judgelog files
judgelogfiles=`find /home/eliseuvidaloca/Desktop/development/sevenonlinejudge/compiler | egrep "\.judgelog$"`

for file in $judgelogfiles
do
    let "judgelogfiles_qtt+=1"
    rm -v $file
done

echo -e "\n------- Program output -------\nc files deleted: $cfiles_qtt;\npyc files deleted: $pycfiles_qtt;\nJudgelog files deleted: $judgelogfiles_qtt;"

