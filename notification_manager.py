from twilio.rest import Client
import smtplib
import os
import email_manager
from pprint import pprint
from datetime import datetime as dt
TWILLIO_API_KEY = os.environ["TWILLIO_API_KEY"]
TWILLIO_ACCOUNT_SID = os.environ["TWILLIO_ACCOUNT_SID"]
MY_TWILLIO_NUMBER = os.environ["MY_TWILLIO_NUMBER"]
CLIENT_NUMBER = os.environ["CLIENT_NUMBER"]
MY_EMAIL = os.environ["MY_EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
stmp_gmail = "smtp.gmail.com"
gmail_port = 587
class NotificationManager:
    def __init__(self,compare_iata_price_list, iata_price_list, from_iata_list):
        self.send_list = []
        self.from_iata_list = from_iata_list
        self.compare_iata_price_list = compare_iata_price_list
        self.iata_price_list = iata_price_list
        city_list = self.iata_price_list.keys()
        for city in city_list:
            if self.iata_price_list[city][0] < self.compare_iata_price_list[city][1]:
                self.send_list.append(city)
        self.generate_message()

    def return_email_city_list(self):
        return self.send_list

    def generate_message(self):
        self.message_list = {}
        for city in self.send_list:
            depature_date = self.date_fix(self.iata_price_list[city][3])
            arrival_date = self.date_fix(self.iata_price_list[city][4])
            message = f"Only ${self.iata_price_list[city][0]} to fly from " \
                      f"{self.from_iata_list[1]}-{self.from_iata_list[0]} to " \
                      f"{self.compare_iata_price_list[city][0]}-{self.iata_price_list[city][2]}.\nFlight Timing: " \
                      f"{depature_date} to " \
                      f"{arrival_date}"
            self.message_list[city]=message


    def date_fix(self, date):
        date_dict = dt(day=int(date[8:10]),month=int(date[5:7]),year=int(date[0:4]),hour=int(date[11:13]),minute=int(date[14:16])).strftime('%B %d %Y, %I:%M %p')
        return(date_dict)

    def generate_link(self, from_date,to_date, from_loc,to_loc):
        from_iata_code=from_loc
        to_iata_code=to_loc
        from_day=from_date[8:10]
        from_month=from_date[5:7]
        from_year=from_date[0:4]
        to_day=to_date[8:10]
        to_month=to_date[5:7]
        to_year=to_date[0:4]
        google_link = f"https://www.google.co.uk/flights?hl=en#flt={from_iata_code}.{to_iata_code}.{from_year}-{from_month}-{from_day}*{to_iata_code}.{from_iata_code}.{to_year}-{to_month}-{to_day}"
        return google_link

    def send_text(self):
        client = Client(TWILLIO_ACCOUNT_SID, TWILLIO_API_KEY)
        for city in self.send_list:
            message = client.messages \
                .create(
                body=f"{self.message_list[city]}",
                from_= MY_TWILLIO_NUMBER,
                to = CLIENT_NUMBER
            )
            print(message.status)



    def send_email(self):
        email_list = self.email_list()
        for email in email_list:
            for city in self.send_list:
                try:
                    message = self.message_list[city]
                    price=self.iata_price_list[city][0]
                    from_city=self.from_iata_list[1]
                    to_city=self.compare_iata_price_list[city][0]
                    duration_of_trip=self.iata_price_list[city][6]

                    book_link=self.generate_link(from_date=self.iata_price_list[city][3],to_date=self.iata_price_list[city][4],from_loc=self.from_iata_list[0],to_loc=self.iata_price_list[city][2])

                    route_text = self.generate_route_list(self.iata_price_list[city][7],from_city,to_city)
                    with smtplib.SMTP(stmp_gmail, port=gmail_port) as connection:
                        connection.starttls()
                        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
                        connection.sendmail(from_addr=MY_EMAIL,
                                            to_addrs=email['email'],
                                            msg=f"Subject:Low Price alert!: {from_city} to {to_city}, {duration_of_trip} day trip for ${price}.\n\n"
                                                 f"Hi {email['firstName']} {email['lastName']},\n{message}.{route_text}\nBook through here: {book_link}")
                except TypeError:
                    pass

    def email_list(self):
        Email_Manager = email_manager.EmailManager()
        return Email_Manager.email_list()

    def generate_route_list(self, route_list,from_city,to_city):
        stop_overs = 0
        route_message = ""
        route_check_list=[from_city,to_city]
        for route in route_list:
            if route not in route_check_list:
                stop_overs += 1
                route_message+= f" via {route}"
                route_check_list.append(route)
        if stop_overs == 1:
            route_message = f"\n\nFlight has {stop_overs} stopover" + route_message + "."
        elif stop_overs != 0:
            route_message = f"\n\nFlight has {stop_overs} stopovers" + route_message + "."
        return route_message

#This class is responsible for sending notifications with the deal flight details.