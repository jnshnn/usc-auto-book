#!/usr/bin/env python3

import uscApi as usc
import time
import datetime

config = usc.loadConfig()
classId = None
i = 0

while i < 24 * 2:
	# each 30 minutes
	timeToWait = i * 30 * 60
	time.sleep(timeToWait)
	i += 1
	print("[main] Tying to find class at %s" % (str(datetime.datetime.now())))
	classId = usc.findDate(config)
	if classId is not None:
		break

if classId is None:
	print("[main] exiting. No Class was found.")
	quit()

print("[main] Log in as user %s " % (config['email']))
token = usc.login(config)
if token is None:
	print("[main] Login failed")
	quit()

print("[main] Login successful")

print("[main] Proceed to book class %s" % (classId))
usc.bookEvent(classId, token, config)



