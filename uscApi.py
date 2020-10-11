import requests

from datetime import datetime, timedelta
import re
import configparser

def loadConfig(conifg_name = 'usc_api.config'):
	"""
	Load the configuration file from the given path.
	"""

	config = configparser.ConfigParser()
	config.readfp(open(conifg_name))
	return {
		'email': 		config.get('Credentials', 'email'),
		'password': 	config.get('Credentials', 'password'),
		'clientSecret': config.get('Client', 'secret'),
		'clientId': 	config.get('Client', 'id'),
		'baseURL': 		config.get('API', 'baseURL'),
		'headers': {
			'accept-encoding': 		config.get('Headers', 'accept-encoding'),
			'user-agent': 			config.get('Headers', 'user-agent'),
			'accept-language': 		config.get('Headers', 'accept-language'),
		}
	}

def login(config):
	"""
	Login with the given credentials. 
	Retrieve a bearer token that will be needed on booking a class.
	"""

	requestURL = config['baseURL'] + '/auth/token'

	data = {
		'username': config['email'],
		'password': config['password'],
		'client_secret': config['clientSecret'],
		'client_id': config['clientId'],
		'grant_type': 'password'
	}

	print("POST: %s" % (requestURL))
	r = requests.post(requestURL, data=data)
	if(r.status_code != 200):
		print("Could login (status code = %d).\nError message said\n" % (r.status_code))
		print(r.json())
	return r.json()['data']['access_token']


def is_bookable(course):
	return course['bookable'] != 0 and course['freeSpots'] != 0


def findClass(config, locationId = 15238, date=None):
	"""
	Find a class on the given date. 
	Returns the first class found on that day. 
	No authorization is needed here. 
	Periodic request can be obfuscated.

	venueId: defines the id of the venue that shell be choosen. 
			 VenueIds need to be accessed via the API. 
			 Venue ids of web an api do not match.

	date: 	 If no date is given the date in 2 week will be taken. 

	"""
	if(date == None):
		date = datetime.today() + timedelta(weeks=2)

	strDate = date.strftime('%Y-%m-%d')

	requestURL = '%s/courses?courses?forDurationOfDays=1&query=&pageSize=100&page=1&locationId=%d&startDate=%s' % (config['baseURL'], locationId, strDate)
	print("GET: %s" % (requestURL))
	r = requests.get(requestURL, headers=config['headers'])

	data = r.json()['data']
	if(not data['classes']):
		print("Cloud not find any class on the given date date (%s) (status code = %d)." % (strDate, r.status_code))
		return
	first_class = data['classes'][0]
	if is_bookable(first_class):
                print("Returning id %d of class %s on %s." % (first_class['id'], first_class['title'], first_class['startDateTimeUTC']))
                return first_class['id']
	else:
		print("Course not bookable. Spots (%d/%d) {deleted: %s, bookable: %d, booking: %s}" % (first_class['maximumNumber'] - first_class['freeSpots'], first_class['maximumNumber'], first_class['deleted'], first_class['bookable'], first_class['booking']))


def bookEvent(classId, bearer, config):
	"""
	Book the given class. 
	"""
	requestURL = config['baseURL'] + '/bookings'
	print("POST: %s" % (requestURL))

	data = {
		'courseId': classId,
	}

	header = config['headers']
	header['authorization'] = 'Bearer ' + bearer

	r = requests.post(requestURL, data=data, headers=header)

	if(r.status_code != 200):
		print("Could not book event (status code = %d).\nError message said\n" % (r.status_code))
		print(r.json())

	print("Booked appointmentId %d. Booking reference %d" % (classId, r.json()['data']['id']))


