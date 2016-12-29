import requests
import pymysql
import time

def getStops(headers, parameters):
	connection = getConnection()
	url = 'https://transloc-api-1-2.p.mashape.com/stops.json'
	response = requests.get(url, headers = headers, params = parameters).json()
	sql =	"INSERT INTO `stops`(`id`, `name`, `lat`, `lng`, `routes`) " 	\
		  	"VALUES (%s, %s, %s, %s, %s) " 									\
		  	"ON DUPLICATE KEY UPDATE `name`=%s, `lat`=%s, `lng`=%s, `routes`=%s"

	try:
		with connection.cursor() as cursor:
			# STOPS: relevant data = name, routes, stop_id, location
			for row in response['data']:
				name = row['name'].encode('ascii', 'ignore').decode('utf-8')
				lat = row['location']['lat']
				lng = row['location']['lng'] 
				stop_id = row['stop_id']
				routes = str(row['routes'])
				cursor.execute(sql, (stop_id, name, lat, lng, routes, 
					name, lat, lng, routes))
				# print (name)
		connection.commit()

	finally:
		connection.close()

def getRoutes(headers, parameters):
	connection = getConnection()
	url = 'https://transloc-api-1-2.p.mashape.com/routes.json'
	response = requests.get(url, headers = headers, params = parameters).json()
	sql = 	"INSERT INTO `routes`(`id`, `name`, `color`, `is_active`, `is_hidden`, `segments`, `stops`) " \
			"VALUES (%s, %s, %s, %s, %s, %s, %s)" \
			"ON DUPLICATE KEY UPDATE `name`=%s, `color`=%s, `is_active`=%s, `is_hidden`=%s, `segments`=%s, `stops`=%s"

	try:
		with connection.cursor() as cursor:
			for row in response['data']['347']:
				name = row['long_name'].encode('ascii', 'ignore').decode('utf-8')
				route_id = row['route_id']
				segments = str(row['segments'])
				is_active = row['is_active']
				is_hidden = row['is_hidden']
				stops = str(row['stops'])
				color = row['color']
				cursor.execute(sql, (route_id, name, color, is_active, is_hidden, segments, stops, 
					name, color, is_active, is_hidden, segments, stops))
		connection.commit()

	finally:
		connection.close()

def getSegments(headers, parameters):
	connection = getConnection()
	url = 'https://transloc-api-1-2.p.mashape.com/segments.json'
	response = requests.get(url, headers = headers, params = parameters).json()
	sql = 	"INSERT INTO `segments`(`id`, `polyline`) " \
			"VALUES (%s, %s)" \
			"ON DUPLICATE KEY UPDATE `polyline`=%s"

	try:
		with connection.cursor() as cursor:
			for segment in response['data']:
				polyline = response['data'][segment]
				# print (polyline)
				cursor.execute(sql, (segment, polyline, polyline))
		connection.commit()

	finally:
		connection.close()

def getArrivals(headers, parameters):
	connection = getConnection()
	url = 'https://transloc-api-1-2.p.mashape.com/arrival-estimates.json'
	response = requests.get(url, headers = headers, params = parameters).json()
	sql = 	"INSERT INTO `stops`(`id`, `arrivals`) " \
			"VALUES (%s, %s)" \
			"ON DUPLICATE KEY UPDATE `arrivals`=%s"

	try:
		with connection.cursor() as cursor:
			for row in response['data']:
				stop_id = row['stop_id']
				arrivals = str(row['arrivals'])
				cursor.execute(sql, (stop_id, arrivals, arrivals))
		connection.commit()

	finally:
		connection.close()

def getConnection():
	return pymysql.connect(
		host='localhost', 
		user='root', 
		password='pass', 
		db='uva', 
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
	headers = {'X-Mashape-Key': 'CwYowCwhaVmshCbsGzvBFhXBXjprp1FdIQkjsnYrOa6UKkiZBF', 'Accept': 'application/json'}
	# Hard-coded for UVA until the time comes to change it
	parameters = {'format': 'json', 'agencies': '347', 'callback': 'call'}
	while True:
		# getStops(headers, parameters)
		getRoutes(headers, parameters)
		# getSegments(headers, parameters)
		getArrivals(headers, parameters)
		print ('Updated at ' + str(time.time()), flush = True)
		time.sleep(2)
