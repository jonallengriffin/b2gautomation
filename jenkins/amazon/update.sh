#!/bin/bash

PWD=`dirname $0`

REMOTE_DIR="/data/jenkins/jobs"

for i in `ssh ec2-user@ec2-107-20-108-245.compute-1.amazonaws.com ls $REMOTE_DIR`
do
    echo $i
    if [ ! -d $i ]; then
      mkdir $i
    fi
    scp ec2-user@ec2-107-20-108-245.compute-1.amazonaws.com:$REMOTE_DIR/$i/config.xml $PWD/$i/config.xml
done

