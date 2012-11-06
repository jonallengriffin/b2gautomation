#!/bin/bash

PWD=`dirname $0`

if [ ! -d "nightly" ]; then
    mkdir nightly
fi
if [ ! -d "stable" ]; then
    mkdir stable
fi
if [ ! -d "unagi" ]; then
    mkdir unagi
fi

REMOTE_NIGHTLY_DIR="/data/update-channels/nightly"
REMOTE_STABLE_DIR="/data/update-channels/stable"
REMOTE_UNAGI_DIR="/data/update-channels/unagi"

for i in `ssh ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com "cd $REMOTE_UNAGI_DIR && ls *.sh update*.xml"`
do
    echo $i
    scp ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com:$REMOTE_UNAGI_DIR/$i $PWD/unagi/$i
done

for i in `ssh ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com "cd $REMOTE_NIGHTLY_DIR && ls *.sh update*.xml"`
do
    echo $i
    scp ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com:$REMOTE_NIGHTLY_DIR/$i $PWD/nightly/$i
done

for i in `ssh ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com "cd $REMOTE_STABLE_DIR && ls *.sh update*.xml"`
do
    echo $i
    scp ec2-user@ec2-184-73-70-191.compute-1.amazonaws.com:$REMOTE_STABLE_DIR/$i $PWD/stable/$i
done
