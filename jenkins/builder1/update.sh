#!/bin/bash

PWD=`dirname $0`

REMOTE_DIR="/data/jenkins/jobs"

for i in `ssh builder1.ateam.phx1.mozilla.com ls $REMOTE_DIR`
do
    echo $i
    if [ ! -d $i ]; then
      mkdir $i
    fi
    scp builder1.ateam.phx1.mozilla.com:$REMOTE_DIR/$i/config.xml $PWD/$i/config.xml
done

