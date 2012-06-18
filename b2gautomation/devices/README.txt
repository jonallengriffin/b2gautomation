This package contains a copy of B2G you can flash on your device.  To perform
the flash, run the command:

    ./flash.sh

Requirements
============

The flash script requires adb, plus either fastboot or heimdall, depending
on your device.

Galaxy-S2: uses adb and heimdall
Nexus-S or Otoro: uses adb and fastboot

The flash script works best on linux, but you may be able to use it on
other operating systems by installing adb and heimdall or fastboot using
the instructions below.

ADB
---
The flash script will attempt to use adb that is found on your system's PATH.
If none is present, it will default to a linux-32 version in this
package, or will generate an error if you are not running this script on
a linux system.

If you are not running on a linux system, or encounter problems with the
bundled adb, you can install adb by installing the Android SDK Starter
Package, and then launching the Android SDK Manager to install the SDK
Platform Tools.  This is steps #2 and #4 at 
http://developer.android.com/sdk/installing.html.  You do not need to install
Eclipse or other SDK plugins.

FASTBOOT
--------
The flash script will attempt to use fastboot that is found on your system's
PATH.  If none is present, it will default to a linux-32 version in this
package, or will generate an error if you are not running this script on
a linux system.

If you are not running on a linux system, or encounter problems with the
bundled fastboot, you can install fastboot by downloading an older version
of the Android SDK at http://developer.android.com/sdk/older_releases.html;
use version Release 1.6 r1.  After you have downloaded this, you can find
fastboot in the "tools" directory.  Place this somewhere on your system's
PATH.

HEIMDALL
--------
Heimdall is not bundled in this package; in order to flash you will need
to install heimdall yourself.  See download links at:
http://www.glassechidna.com.au/products/heimdall/

