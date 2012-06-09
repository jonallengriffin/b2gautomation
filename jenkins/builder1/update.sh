#!/bin/bash

PWD=`dirname $0`

REMOTE_DIR="/data/jenkins/jobs"

#scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-emulator-arm/config.xml $PWD/build-emulator-arm/config.xml
#scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-emulator-x86/config.xml $PWD/build-emulator-x86/config.xml
#scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-nexus-s/config.xml $PWD/build-nexus-s/config.xml
#scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-sgs2/config.xml $PWD/build-sgs2/config.xml

for i in `ssh builder1.ateam.phx1.mozilla.com ls $REMOTE_DIR`
do
    echo $i
    if [ ! -d $i ]; then
      mkdir $i
    fi
    scp builder1.ateam.phx1.mozilla.com:$REMOTE_DIR/$i/config.xml $PWD/$i/config.xml
done

