import requests
import os
import time
from pprint import pprint
TEQUILLA_API_KEY = os.environ["TEQUILLA_API_KEY"]
TEQUILLA_URL = "https://tequila-api.kiwi.com/locations/query"

class FlightData():
    def __init__(self, city_iata_list):
        self.filled_iata_list = []
        tequilla_headers = {
            "apikey": TEQUILLA_API_KEY
        }
        for city in city_iata_list:
            city_name = city["city"]
            tequilla_params = {
                "term": city_name,
                "locale": "en-US",
                "location_types": "airport",
                "active_only": True
            }
            response = requests.get(url=TEQUILLA_URL, headers=tequilla_headers, params=tequilla_params)
            response.raise_for_status()
            city_response_data = response.json()
            try:
                city_dict = {'city': city["city"], 'iataCode': city_response_data["locations"][0]["city"]["code"], 'id': city["id"], 'lowestPrice': city["lowestPrice"]}
            except KeyError:
                pass
            self.filled_iata_list.append(city_dict)

    def iata_code_list(self):
        return self.filled_iata_list


    #This class is responsible for structuring the flight data.