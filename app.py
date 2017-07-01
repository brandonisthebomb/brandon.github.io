import requests
import os
import json
from flask import Flask, request, make_response, render_template, send_from_directory
from geopy.distance import vincenty

app = Flask(__name__)

BUS_AGENCY_ID = '347'
USERS = ['brandon']

# Handle the index case for blank url.
@app.route('/')
def index():
	return render_template('index.html')

# Route for handling the login page logic.
@app.route('/login', methods=['GET', 'POST'])
def login():
	data = request.form
	user = data.get("user")
	if user.lower() == 'brandon':
		return make_response("OK", 200)
	else:
		return make_response("NOT OK", 500)

@app.route('/bus', methods=['GET','POST']) 	 
def bus():
	# Handle GET
	if request.method == 'GET':
		return render_template('bus.html')

	# Handle POST
	elif request.method == 'POST':
		lat = ''; lng = ''
		if request.is_json:
			data = request.get_json()
			lat = data['lat']
			lng = data['lng']
		else:
			data = request.form
			lat = data.get('lat')
			lng = data.get('lng')
			print('Lat: %s, Long: %s' % (lat, lng))
		calculate_bus(lat, lng)

		return make_response("OK", 200)

def calculate_bus(lat, lng):
	headers = { 'X-Mashape-Key': 'CwYowCwhaVmshCbsGzvBFhXBXjprp1FdIQkjsnYrOa6UKkiZBF',
	'Accept': 'application/json' }
	params = { 'agencies': BUS_AGENCY_ID } 
	response = requests.get('https://transloc-api-1-2.p.mashape.com/stops.json', headers=headers, params=params)
	# pretty_print_json(response.json()) 
	data = response.json()['data']

	# for stop in data:
	# 	name = stop['name']
	# 	lat = stop['location']['lat']
	# 	lng = stop['location']['lng']
	# 	print('%s %s %s' % (name, lat, lng))
	print(min_dist(lat, lng, data))

def min_dist(lat, lng, stops):
	min_dist = float('inf')
	closest_stop = ''
	for stop in stops:
		target_lat = stop['location']['lat']
		target_lng = stop['location']['lng']
		dist = vincenty((lat, lng), (target_lat, target_lng)).miles
		if dist < min_dist:
			min_dist = dist
			closest_stop = stop
		print(dist)

def pretty_print_json(input):
    print (json.dumps(input, indent=4))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
	app.run(debug=True)