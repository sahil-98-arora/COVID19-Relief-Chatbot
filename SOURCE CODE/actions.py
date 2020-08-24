# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
#
import numpy as np
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import smtplib
import requests
#



# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://api.covid19india.org/data.json").json()
        
        entities = tracker.latest_message['entities']
        print("latest message now ", entities)
        state = None
        for e in entities:
            if e['entity'] == "state":
                state = e['value']
        
        message = "Please enter correct state name !"
        if state == "india":
            state = "Total"
        if state == "India":
            state = "Total"
        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Active: "+data["active"] + "\nConfirmed: "+data["confirmed"] + "\nRecovered: "+data["recovered"] + "\nDeaths: "+data["deaths"] + "\nas on "+data["lastupdatedtime"]
                
        dispatcher.utter_message(text=message)

        return []


class ActionBmsDisplayMenu(Action):

    def name(self) -> Text:

        return "action_BMS_display_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        conn = sqlite3.connect('bms.db')
        user_message = str((tracker.latest_message)['text'])

        print("User message : ", user_message)
        if "women" in user_message:
            exe_str = "Select choice, price from bms1 where gender is '{0}'".format('women')
        elif "men" in user_message:
            exe_str = "Select choice, price from bms1 where gender is '{0}'".format('men')

        content = conn.execute(exe_str)
        content_text = ''
        for index, value in enumerate(content):
            content_text += str(index + 1) + ") " + str(value[0]) + "  ----  " + str(value[1]) + "/-\n"

        content_text += "Enter item numbers (eg : 1,2,4)"
        dispatcher.utter_message(text=content_text)

        return []


class ActionBmsOrderRecieved(Action):

    def name(self) -> Text:

        return "action_bms_order_recieved"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = sqlite3.connect('bms.db')
        user_message = str((tracker.latest_message)['text'])

        messages = []

        for event in (list(tracker.events))[:1000]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        print("messages : ",messages)

        user_email = messages[-1]
        print("user_email : ",user_email)
        if "@" in user_email:
            toaddrs = user_email

        user_message = messages[-3]
        print("user_message : ",user_message)
        

        for_gender = ''
        if 'women' in user_message:
            exe_str = "Select choice, price from bms1 where gender is '{0}'".format('women')
            for_gender = "FOR WOMEN"

        elif "men" in user_message:
            exe_str = "Select choice, price from bms1 where gender is '{0}'".format('men')
            for_gender = "FOR MEN"



        try:
            content = conn.execute(exe_str)
        
            user_input = messages[-2]
            user_input = user_input.replace(" ", "")
            # user_input = user_input.split(',')
            user_input = [int(n) for n in user_input.split(',')]
            print("user_input : ", user_input)

            total = 0
            content_text = ''
            choices_ = ''
            for index, value in enumerate(content):
                if index + 1 in user_input:
                    total += value[1]
                    choices_ += value[0] + '\n'

            bill_no = np.random.randint(1,1000,1)[0]

            fromaddr = 'YOUR EMAIL ADDRESS'
            #toaddrs = 'TO EMAIL ADDRESS'
        
            #######
            msg = "Hello! This is your confirmation email from BIGMAN SALON. Your booking " + for_gender + " is confirmed for tomorrow .\n\nThe following are the choices you have made for the booking no " \
                    + str(bill_no) + "\n\nchoices : \n" + choices_ + "\nYour total order is Rs " + str(total)+"\n\nOur person will soon contact you tomorrow for anyother help please contact  Phone no: 97166XXXX6\n\nThanks,\nYour own online salon in partner with Covid Relief!"
            #######

            username = 'YOUR EMAIL ADDRESS'
            obj = open('pass.txt')
            password = obj.read()
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()

            content_text = "Your booking has been received and your total order is Rs" + str(total) + \
                            " and your bill number is " + str(bill_no) +". "
            dispatcher.utter_message(text=content_text)
           
        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []


class ActionNmDisplayMenu(Action):

    def name(self) -> Text:

        return "action_NM_display_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        conn = sqlite3.connect('nm.db')
        user_message = str((tracker.latest_message)['text'])

        print("User message : ", user_message)
        if "corona protection" in user_message:
            exe_str = "Select choice, price from nm1 where category is '{0}'".format('corona protection')
        elif "medicine" in user_message:
            exe_str = "Select choice, price from nm1 where category is '{0}'".format('medicine')

        content = conn.execute(exe_str)
        content_text = ''
        for index, value in enumerate(content):
            content_text += str(index + 1) + ") " + str(value[0]) + "  ----  " + str(value[1]) + "/-\n"

        content_text += "Enter item numbers (eg : 1,2,4)"
        dispatcher.utter_message(text=content_text)

        return []


class ActionNmOrderRecieved(Action):

    def name(self) -> Text:

        return "action_nm_order_recieved"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = sqlite3.connect('nm.db')
        user_message = str((tracker.latest_message)['text'])

        messages = []

        for event in (list(tracker.events))[:1000]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        print("messages : ",messages)

        user_email = messages[-1]
        print("user_email : ",user_email)
        if "@" in user_email:
            toaddrs = user_email

        user_message = messages[-3]
        print("user_message : ",user_message)
        

        for_category = ''
        if 'corona protection' in user_message:
            exe_str = "Select choice, price from nm1 where category is '{0}'".format('corona protection')
            for_category = "CORONA PROTECTION"

        elif "medicine" in user_message:
            exe_str = "Select choice, price from nm1 where category is '{0}'".format('medicine')
            for_category = "MEDICINE"



        try:
            content = conn.execute(exe_str)
        
            user_input = messages[-2]
            user_input = user_input.replace(" ", "")
            # user_input = user_input.split(',')
            user_input = [int(n) for n in user_input.split(',')]
            print("user_input : ", user_input)

            total = 0
            content_text = ''
            choices_ = ''
            for index, value in enumerate(content):
                if index + 1 in user_input:
                    total += value[1]
                    choices_ += value[0] + '\n'

            bill_no = np.random.randint(1,1000,1)[0]

            fromaddr = 'YOUR EMAIL ADDRESS'
            #toaddrs = 'TO EMAIL ADDRESS'
        
            #######
            msg = "Hello! This is your confirmation email from NETMEDS. Your order for " + for_category + " category is confirmed and will be delivered at your doorstep asap.\n\nThe following are the choices you have made for order no " \
                    + str(bill_no) + "\n\nchoices : \n" + choices_ +"\nYour total order is Rs " + str(total)+"\n\nThanks,\nYour own online pharmacy in partner with Covid Relief!"
            #######

            username = 'YOUR EMAIL ADDRESS'
            obj = open('pass.txt')
            password = obj.read()
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()

            content_text = "Your order has been received and your total order is Rs" + str(total) + \
                            " and your order number is " + str(bill_no) +". "
            dispatcher.utter_message(text=content_text)
           
        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []


