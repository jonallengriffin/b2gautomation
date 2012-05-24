#!/bin/bash

OS=`uname -s | tr "[[:upper:]]" "[[:lower:]]"`

ADB=${ADB:-adb}
HEIMDALL=${HEIMDALL:-heimdall}

if [ ! -f "`which \"$ADB\"`" ]; then
	if [ "$OS" != "linux" ]; then
		echo "adb not found on your PATH, and this package does not contain"
		echo "an adb appropriate for your system; see README.txt"
		exit = -1
	fi
	ADB=./adb
fi

if [ ! -f "`which \"$HEIMDALL\"`" ]; then
	echo "heimdall not found on your PATH, see README.txt"
	exit -1
fi

update_time()
{
	echo "Attempting to set the time on the device..."
	sleep 5
	$ADB wait-for-device &&
	$ADB shell toolbox date `date +%s` &&
	$ADB shell setprop persist.sys.timezone `date +%Z%:::z|tr +- -+` || exit -1
}

flash_heimdall()
{
	echo "Attempting to reboot the phone into download mode...."
	$ADB reboot download || echo "Couldn't reboot into download mode. Hope you're already in download mode"
	sleep 8

	echo "Flashing system and kernel images...."
	$HEIMDALL flash --factoryfs system.img --kernel kernel || exit -1
}

update_gaia()
{
	echo "Updating with latest Gaia..."
	sleep 5
	$ADB wait-for-device shell rm -rf /cache/* &&
	$ADB shell rm -rf /data/local/* &&
	$ADB push local /data/local &&
	$ADB reboot || exit -1
}

flash_heimdall
update_gaia
update_time


