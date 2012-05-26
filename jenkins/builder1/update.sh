#!/bin/bash

PWD=`dirname $0`

scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-emulator-arm/config.xml $PWD/build-emulator-arm/config.xml
scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-emulator-x86/config.xml $PWD/build-emulator-x86/config.xml
scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-nexus-s/config.xml $PWD/build-nexus-s/config.xml
scp jgriffin@builder1.ateam.phx1.mozilla.com:/data/jenkins/jobs/build-sgs2/config.xml $PWD/build-sgs2/config.xml

