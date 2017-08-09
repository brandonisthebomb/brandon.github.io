class Stop:

    def __init__(self, name, stop_id, latitude, longitude, routes):
        self.name = name
        self.stop_id = stop_id
        self.latitude = latitude
        self.longitude = longitude
        self.routes = routes

    def init_from_json(json):
        stop = Stop(json['name'])
        return stop
