ADB = ./adb
HEIMDALL = heimdall

.PHONY: flash
flash: flash-image update-time

.PHONY: flash-image
flash-image:
	echo Flashing kernel and system ...
	- $(ADB) reboot download && \
	sleep 20
	$(HEIMDALL) flash --kernel kernel --factoryfs system.img && \
	echo done
	echo Updating gecko ... && \
	sleep 5 && \
	$(ADB) wait-for-device push b2g system/b2g && \
	echo done
	echo Updating gaia ... && \
	$(ADB) shell rm -rf /cache/* && \
	$(ADB) shell rm -rf /data/local/* && \
	$(ADB) push local /data/local && \
	$(ADB) reboot && \
	echo done

TIMEZONE ?= $(shell date +%Z%:::z|tr +- -+)
.PHONY: update-time
update-time:
	@echo "|make update-time TIMEZONE=<zone>| to set timezone"
	sleep 5
	$(ADB) wait-for-device shell toolbox date `date +%s`
	$(ADB) shell setprop persist.sys.timezone $(TIMEZONE)
