import requests
import os
import json
from pprint import pprint
import datetime as dt
import time
FROM = dt.date.today().strftime("%d/%m/%Y")
TO = (dt.date.today() + dt.timedelta(days=180)).strftime("%d/%m/%Y")
TEQUILLA_API_KEY = os.environ["TEQUILLA_API_KEY"]
BRANDLY_API_KEY = os.environ["BRANDLY_API_KEY"]
TEQUILLA_URL = "https://tequila-api.kiwi.com/v2/search"
BRANDLY_URL = "https://api.rebrandly.com/v1/links"
tequilla_headers = {
    "apikey" : TEQUILLA_API_KEY
}
brandly_headers = {
    "Content-type": "application/json",
    "apikey": BRANDLY_API_KEY
}

class FlightSearch:
    def __init__(self, city_iata_list, from_iata):
        city_list = city_iata_list.keys()
        self.lowest_prices={}
        city_list=city_iata_list.keys()
        for city in city_list:
            lowest_fair_by_airport={}
            price_list = []
            tequilla_params = {
                "fly_from" : f"city:{from_iata[0]}",
                "fly_to" : city,
                "date_from":FROM,
                "date_to":TO,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 14,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 2,
                'stopover_to': '04:00',
                "curr":"CAD"
            }
            response = requests.get(url=TEQUILLA_URL, headers=tequilla_headers, params=tequilla_params)
            response.raise_for_status()
            response_data = response.json()
            try:
                url_shortner_praram = {
                    'destination': response_data["data"][0]["deep_link"]
                }
                brandly_response = requests.post(url=BRANDLY_URL, data=json.dumps(url_shortner_praram),
                                                 headers=brandly_headers)
                brandly_response.raise_for_status()
                brandly_data = brandly_response.json()
                short_url = brandly_data['shortUrl']
                route_list = []
                for route in response_data["data"][0]['route']:
                        route_list.append(route['cityFrom'])
                self.lowest_prices[city] = [response_data["data"][0]["price"], response_data["data"][0]["flyFrom"],
                                            response_data["data"][0]["flyTo"], response_data["data"][0]['route'][0]["local_departure"],
                                            response_data["data"][0]['route'][-1]["local_arrival"], short_url, response_data["data"][0]['nightsInDest'], route_list]
            except IndexError:
                pass



    def get_lowest_price(self):
        return self.lowest_prices

    #This class is responsible for talking to the Flight Search API.