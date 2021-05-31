import requests
import os
from pprint import pprint
#Updated through https://replit.com/@CliveNazareth/FlightDealList#main.py
SHEETY_USERNAME = os.environ['SHEETY_USERNAME']
SHETTY_ENDPOINT = F"https://api.sheety.co/{SHEETY_USERNAME}/flightDeals/users"
SHEETY_BEARER = os.environ['SHEETY_BEARER']


class EmailManager:
    def __init__(self):
        sheet_headers = {
            "Authorization" : f"Bearer {SHEETY_BEARER}"
            }
        response = requests.get(url=SHETTY_ENDPOINT, headers=sheet_headers)
        response.raise_for_status()
        self.response_data = response.json()


    def email_list(self):
        return self.response_data['users']