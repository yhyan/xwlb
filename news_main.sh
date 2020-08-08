#!/usr/bin/env bash

SRCDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo `date`
echo $PATH
env
python $SRCDIR/news_xwlb.py $1
python $SRCDIR/news_content.py $1
python $SRCDIR/news_keys.py $1

echo 'finish'



