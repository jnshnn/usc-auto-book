#!/usr/bin/env python3

import uscApi as usc
import time
import datetime

config = usc.loadConfig()
classId = None
i = 0
# each 30 minutes
timeToWait = 30 * 60

while i < 24 * 2: # run for 24h each 30 minutes
	print("[main] Tying to find class at %s" % (str(datetime.datetime.now())))

	# when running longer then 24h we need to persist the date
	targetDate = datetime.today() + timedelta(weeks=2)

	classId = usc.findDate(config, date = targetDate)
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



