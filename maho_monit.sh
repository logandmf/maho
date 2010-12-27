#!/bin/bash

ppid=$(pgrep -P `cat /var/run/maho.pid`) || ppid="NULL"

if [ "$ppid" == "NULL" ]; then
	/etc/init.d/maho stop
	/etc/init.d/maho start
fi
