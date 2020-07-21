#!/usr/bin/env bash

# rsync local change to remote machine

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOCAL_DIR=`git rev-parse --show-toplevel`
REMOTE_DIR="/data/gh/"

if [ -z $1  ]; then
    REMOTE_HOST='yhyan'
else
    REMOTE_HOST=$1
fi

echo
echo LOCAL_DIR=$LOCAL_DIR
echo REMOTE=$REMOTE_HOST:$REMOTE_DIR

rsync -avz --delete\
      --exclude-from=$SCRIPT_DIR/.gitignore\
      --exclude='.git'\
      $LOCAL_DIR $REMOTE_HOST:$REMOTE_DIR
exit

#      --exclude='*.pyc'\
#
#      --exclude='.cache'\
#      --exclude='.idea'\
#      --exclude='sync_code.sh'\
