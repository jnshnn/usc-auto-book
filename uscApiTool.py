#!/usr/bin/env python3

import uscApi as usc
import time
import datetime

config = usc.loadConfig()
classId = None
i = 0
# each 30 minutes
timeToWait = 30 * 60

while i < 17 * 2: # run for 17h each 30 minutes
	print("[main] Tying to find class at %s" % (str(datetime.datetime.now())))
	classId = usc.findDate(config)
	if classId is not None:
		break

	time.sleep(timeToWait)
	i += 1


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



