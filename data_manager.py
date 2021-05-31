import requests
import os
from pprint import pprint
import flight_data
SHEETY_USERNAME = os.environ["SHEETY_USERNAME"]
SHETTY_ENDPOINT = F"https://api.sheety.co/{SHEETY_USERNAME}/flightDeals/prices"
SHEETY_BEARER = os.environ["SHEETY_BEARER"]
class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.city_list=[]
        self.price_list={}
        sheet_headers = {
            "Authorization" : f"Bearer {SHEETY_BEARER}"
        }
        shetty_reponse = requests.get(url=SHETTY_ENDPOINT, headers = sheet_headers)
        shetty_reponse.raise_for_status()
        shetty_data = shetty_reponse.json()
        self.shetty_price_data = shetty_data["prices"]

    def iata_code_update(self):
        FlightData = flight_data.FlightData(self.shetty_price_data)
        self.shetty_price_data = FlightData.iata_code_list()
        sheet_headers = {
            "Authorization" : f"Bearer {SHEETY_BEARER}"
        }
        for city in self.shetty_price_data:
            Sheety_row_endpoint = SHETTY_ENDPOINT + "/" + str(city['id'])
            row = {
                "price" : {
                    "city": city['city'],
                    "iataCode": city['iataCode'],
                    "lowestPrice": city['lowestPrice']
                }
            }
            sheety_row = requests.put(url=Sheety_row_endpoint, headers=sheet_headers, json=row)
            sheety_row.raise_for_status()

    def prices_iata_code(self):
        for row in self.shetty_price_data:
            self.price_list[row["iataCode"]] = [row["city"], row["lowestPrice"]]
        return self.price_list


