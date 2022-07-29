import requests
from base64 import b64encode
import json
import pandas as pd 
from dotenv import load_dotenv
import os
from datetime import datetime


def generate_Dates():
    # now = datetime.now()

    # day = now.day
    # month = now.month
    # year = now.year

    # if day < 10:
    #     day = "0" + str(day)

    # if month < 10:
    #     month = "0" + str(month)
        
   
     
    # today = str(month)  + "-" + str(day) + "-" + str(year)
    # from_date = today + " 00:00:00"
    # to_date  = today + " 23:59:59"

    from_date = "07-27-2022 00:00:00"
    to_date = "07-27-2022 23:59:59"
    return [from_date, to_date]


#Works with the .env file and helps to keep the API key secure (A matching .env file will have to be setup on any machine running this code)
#The purpose of a .env file is to hide any environment variables that contain information that needs to be hidden api_keys, passwords... etc
#This has to be called before anything else in order for the request to be made using the key
def configure():
    load_dotenv()   #This function is from the dotenv library

#fetches data using azugas TRIP api call 
#Returns the data in JSON format
#https://developer.azuga.com/docs/activity <---- Documentation found here
def request_trips():
    
    dates = generate_Dates()
    #Provided URL for this call
    url = 'https://api.azuga.com/azuga-ws/v1/activity/list.json'

    #Required headers (specified in documentation)
    #Key has to encoded (Encoded key is found in .env file)
    headers = {'Authorization': 'Basic {}'.format(os.getenv('encoded_key'))}

    #Parameters required for the call
    parameter = {
        'allGroupsReport': 'true',
        'from': dates[0], #Start date and time for desired range (UTC)
        'to': dates[1],    #End date and time for desired range (UTC)
    }

    #Returns a response object that contains all the data from the call 
    response = requests.get(url, headers=headers, params = parameter)

    return json.loads(response.text)

def get_all_trips(pages):
    for page in range(pages):
        dates = generate_Dates()
        #Provided URL for this call
        url = 'https://api.azuga.com/azuga-ws/v1/activity/list.json'

        #Required headers (specified in documentation)
        #Key has to encoded (Encoded key is found in .env file)
        headers = {'Authorization': 'Basic {}'.format(os.getenv('encoded_key'))}

        #Parameters required for the call
        parameter = {
            'allGroupsReport': 'true',
            'from': dates[0], #Start date and time for desired range (UTC)
            'to': dates[1],    #End date and time for desired range (UTC)
            'page': page
        }

        #Returns a response object that contains all the data from the call 
        response = requests.get(url, headers=headers, params = parameter)
        json_data = json.loads(response.text)
        df = pd.DataFrame(json_data['activityResponseVO']['activityReport'])
        df.to_csv("data_July.csv", mode = 'a', index = False, header= False)


def main():

    #ensure configure runs before anything else 
    configure()

    #Turn JSON data into a dicionary to handle data easier
    json_dict =  request_trips()
    #print(json_dict)

    #Turn data into a pandas dataFrame
    df = pd.DataFrame(json_dict['activityResponseVO']['activityReport'])
    #Write the data to a csv
    df.to_csv("data_July.csv", mode = 'a', index = False, header= False)

    total_pages = (json_dict['activityResponseVO']['totalPages'])
    get_all_trips(total_pages)

#Driver code
main()

