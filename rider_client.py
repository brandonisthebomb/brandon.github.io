import requests

class RiderClient:

    BASE_URL = "https://transloc-api-1-2.p.mashape.com"

    FORMAT = "json"

    STOPS = "stops"


    UVA_ID = ["347"]

    def __init__(self):
        pass

    def __construct_request_url(self, endpoint, format):
        """
        Construct the request URL.
        :param endpoint: the Rider endpoint to use (i.e. stops, routes)
        :param format: the request format, either json or jsonp
        :return: a string containing the full request url
        """
        return "%s/%s.%s" % (self.BASE_URL, endpoint, format)

    def __get(self, request_url, headers, params):
        """
        Make a GET request to the Rider API.
        :param request_url: the request url for the Rider endpoint
        :param headers: the request headers
        :param params: the request parameters
        :return: the response from the GET request
        """
        return requests.get(request_url, headers=headers, params=params)

    def get_stops(self, agency_ids=UVA_ID, geo_area=None, format=FORMAT):

        assert format == "json" or format == "jsonp", "format must be 'json' or 'jsonp'"
        agency_ids = ','.join(agency_ids)
