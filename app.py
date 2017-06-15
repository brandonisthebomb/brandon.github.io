import requests
import googlemaps
import os
from flask import Flask, request, make_response, render_template, send_from_directory
from uuid import getnode as get_mac

app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyAjIfjgEkNuc_HI8_IAV1qm3hGir30hEmY')

GMAPS_API_KEY='AIzaSyAHjg4qV9Q0D3CHyQZ0rZseteIHOXPikGw'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bus', methods=['GET','POST']) 	 
def bus():
	if request.method == 'GET':
		return render_template('bus.html')
	else:
		if request.is_json:
			data = request.get_json()
			lat = data['lat']
			lng = data['lng']
		else:
			data = request.form
			lat = data.get('lat')
			lng = data.get('lng')
			print(lat)
			print(lng)

		return make_response("OK", 200)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
	app.run(debug=True)