ADB = ./adb
FASTBOOT = ./fastboot

.PHONY: flash
flash: flash-image update-time

.PHONY: flash-image
flash-image:
	-	$(ADB) reboot bootloader
	- $(FASTBOOT) oem unlock
	export ANDROID_PRODUCT_OUT="./" && \
	$(FASTBOOT) devices && \
	$(FASTBOOT) erase cache && \
	$(FASTBOOT) erase userdata && \
	$(FASTBOOT) flash userdata userdata.img && \
	$(FASTBOOT) flash boot boot.img && \
	$(FASTBOOT) flash system system.img && \
	$(ADB) reboot

TIMEZONE ?= $(shell date +%Z%:::z|tr +- -+)
.PHONY: update-time
update-time:
	@echo "|make update-time TIMEZONE=<zone>| to set timezone"
	$(ADB) wait-for-device
	$(ADB) shell toolbox date `date +%s`
	$(ADB) shell setprop persist.sys.timezone $(TIMEZONE)
