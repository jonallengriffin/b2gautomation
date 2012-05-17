ADB = ./adb
HEIMDALL = heimdall

.PHONY: flash
flash: flash-image update-time

.PHONY: flash-image
flash-image:
	- $(ADB) reboot recovery
	sleep 30 && \
	echo -n Erasing /data ... && \
	$(ADB) shell mount data && \
	$(ADB) shell rm -r /data/* && \
	echo done && \
	echo -n Erasing /cache ... && \
	$(ADB) shell mount cache && \
	$(ADB) shell rm -r /cache/* && \
	echo done && \
	echo -n Installing gaia ... && \
	$(ADB) push local /data/local && \
	echo done
	echo -n Flashing kernel and system ... && \
	$(ADB) reboot download && \
	sleep 20 && \
	$(HEIMDALL) flash --kernel kernel --factoryfs system.img && \
	echo done

TIMEZONE ?= $(shell date +%Z%:::z|tr +- -+)
.PHONY: update-time
update-time:
	@echo "|make update-time TIMEZONE=<zone>| to set timezone"
	sleep 60
	$(ADB) shell toolbox date `date +%s`
	$(ADB) shell setprop persist.sys.timezone $(TIMEZONE)
