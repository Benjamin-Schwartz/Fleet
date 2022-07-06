import requests
from base64 import b64encode
import json
import pandas as pd 
from dotenv import load_dotenv
import os


#Works with the .env file and helps to keep the API key secure (A matching .env file will have to be setup on any machine running this code)
#The purpose of a .env file is to hide any environment variables that contain information that needs to be hidden api_keys, passwords... etc
#This has to be called before anything else in order for the request to be made using the key
def configure():
    load_dotenv()   #This function is from the dotenv library


#fetches data using azugas TRIP api call 
#Returns the data in JSON format
#https://developer.azuga.com/docs/activity <---- Documentation found here
def request_trips():
    
    #Provided URL for this call
    url = 'https://api.azuga.com/azuga-ws/v1/activity/list.json'


    #Required headers (specified in documentation)
    #Key has to encoded (Encoded key is found in .env file)
    headers = {'Authorization': 'Basic {}'.format(os.getenv('encoded_key'))}

    #Parameters required for the call
    parameter = {
        'groupName': 'Default Group',
        'from': '07-05-2022 00:00:00', #Start date and time for desired range (UTC)
        'to': '07-05-2022 12:55:00'    #End date and time for desired range (UTC)
    }


    #Returns a response object that contains all the data from the call 
    response = requests.get(url, headers=headers, params = parameter)

    #Return the data in JSON format
    return json.loads(response.text)


def main():

    #ensure configure runs before anything else 
    configure()


    #Turn JSON data into a dicionary to handle data easier
    json_dict =  request_trips()

    #Turn data into a pandas dataFrame
    df = pd.DataFrame(json_dict['activityResponseVO']['activityReport'])

    #Write the data to a csv
    df.to_csv("test.csv", index = False)

#Driver code
main()


