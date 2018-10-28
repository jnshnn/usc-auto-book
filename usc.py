import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def login(email, password):
	requestURL = 'https://urbansportsclub.com/en/login'
	print("GET: %s" % (requestURL))
	r = requests.get(requestURL)

	parsed_html = BeautifulSoup(r.text)
	hiddenValue = parsed_html.body.find(id="login-form").findAll("input")[0]
	additional_name = hiddenValue["name"]
	additional_value = hiddenValue["value"]

	data = {
		'email': email,
		'password': password,
		additional_name: additional_value
	}

	print("POST: %s" % (requestURL))
	r = requests.post('https://urbansportsclub.com/en/login', data=data)
	return r.cookies


def findDate(loc = "east61", date=None, eventTitle = "Community-Beachvolleyballtreff"):
	if(date == None):
		# TODO: change
		date = datetime.today() + timedelta(weeks=2)

	strDate = date.strftime('%Y-%m-%d')
	requestURL = 'https://urbansportsclub.com/en/venues/%s?date=%s' % (loc, strDate)
	print("GET: %s" % (requestURL))
	r = requests.get(requestURL)

	parsed_html = BeautifulSoup(r.text)
	appointmentIds = parsed_html.body.findAll("div", {"data-appointment-id": re.compile(r"[0-9]+")})
	appointmentIds = [ int(div["data-appointment-id"]) for div in appointmentIds]

	print("Found appointmentIds: " + str(appointmentIds))

	for appointmentId in appointmentIds: 
		requestURL = 'https://urbansportsclub.com/en/class-details/%d' % (appointmentId)
		print("GET: %s" % (requestURL))
		r = requests.get(requestURL)
		parsed_html = BeautifulSoup(r.text)

		if(parsed_html.find("h3").text == eventTitle):
			return appointmentId 
	else:
		print("No matching appointments found for date %s and event title '%s'" % (strDate, eventTitle))

def bookEvent(appointmentId, cookies):
	requestURL = 'https://urbansportsclub.com/en/search/book/%d' % (appointmentId)
	print("GET: %s" % (requestURL))

	r = requests.get(requestURL, cookies = cookies)

	if(r.status_code != 200):
		print("Could not book event (status code = %d).\nError message said\n" % (r.status_code))
		print(r.text)

	print("Booked appointmentId %d" % (appointmentId))


