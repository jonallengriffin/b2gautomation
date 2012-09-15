#!/bin/bash

OS=`uname -s | tr "[[:upper:]]" "[[:lower:]]"`

ADB=${ADB:-adb}
FASTBOOT=${FASTBOOT:-fastboot}

if [ ! -f "`which \"$ADB\"`" ]; then
	if [ "$OS" != "linux" ]; then
		echo "adb not found on your PATH, and this package does not contain"
		echo "an adb appropriate for your system; see README.txt"
		exit = -1
	fi
	ADB=./adb
fi

if [ ! -f "`which \"$FASTBOOT\"`" ]; then
	if [ "$OS" != "linux" ]; then
		echo "fastboot not found on your PATH, and this package does not contain"
		echo "a fastboot appropriate for your system; see README.txt"
		exit = -1
	fi
	FASTBOOT=./fastboot
fi

update_time()
{
	echo "Attempting to set the time on the device..."
	sleep 5
	$ADB wait-for-device &&
	$ADB shell toolbox date `date +%s` &&
	$ADB shell setprop persist.sys.timezone `date +%Z%:::z|tr +- -+` || exit -1
}

flash_fastboot()
{
	echo "Rebooting into device bootloader..."
	$ADB reboot bootloader || true
	$FASTBOOT devices &&
	( $FASTBOOT oem unlock || true )

	if [ $? -ne 0 ]; then
		echo Couldn\'t setup fastboot
		exit -1
	fi

	echo "Flashing system images..."
	$FASTBOOT erase cache &&
	$FASTBOOT erase userdata &&
	$FASTBOOT flash userdata userdata.img &&
	$FASTBOOT flash boot boot.img &&
	$FASTBOOT flash system system.img &&
	$FASTBOOT reboot || exit -1
}

flash_fastboot
update_time

