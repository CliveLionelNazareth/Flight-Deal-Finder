import data_manager
import flight_data
import flight_search
import notification_manager
from pprint import pprint
import email_manager
Data_Manager = data_manager.DataManager()
# Data_Manager.iata_code_update()
city_iata_list = Data_Manager.prices_iata_code()
from_iata = ["YYZ", "Toronto"]
Flight_Search = flight_search.FlightSearch(city_iata_list=city_iata_list, from_iata=from_iata)
iata_price_list = Flight_Search.get_lowest_price()
NotificationManager = notification_manager.NotificationManager(compare_iata_price_list=city_iata_list, iata_price_list=iata_price_list, from_iata_list=from_iata)
NotificationManager.send_email()



