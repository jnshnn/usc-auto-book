#!/usr/bin/env python3

import uscApi as usc
import time
from datetime import datetime, timedelta

config = usc.loadConfig()
classId = None
# each 30 minutes
timeToWait = 30 * 60
targetDate = datetime.today() + timedelta(weeks = 2)

while targetDate + timedelta(days=1) > datetime.today(): 
	print("[main] Tying to find class at %s" % (str(datetime.now())))

	classId = usc.findClass(config, date = targetDate)
	if classId is not None:
		break

	time.sleep(timeToWait)


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



