import requests
from base64 import b64encode
import json
import pandas as pd 
from dotenv import load_dotenv
import os
from datetime import datetime


def request_trips():
    
    
    #Provided URL for this call
    url = 'https://api.azuga.com/azuga-ws/v1/vehicle/view.json?'

    #Required headers (specified in documentation)
    #Key has to encoded (Encoded key is found in .env file)
    headers = {'Authorization': 'Basic {}'.format(os.getenv('encoded_key'))}

    #Parameters required for the call
    parameter = {
        'groupName': 'Default Group',
        'includeChildGroups': 'true',
        'page': '2'
    }

    #Returns a response object that contains all the data from the call 
    response = requests.get(url, headers=headers, params = parameter)

    return json.loads(response.text)
    

load_dotenv()

json_dict =  request_trips()
    #print(json_dict)



# #Turn data into a pandas dataFrame
pages = (json_dict['vehicleResponseVO']['totalPages'])
print(pages)
df = pd.DataFrame(json_dict['vehicleResponseVO']['vehicles'])

# print(pages)
#Write the data to a csv
df.to_csv("AllVehicles.csv", mode = 'a', index = False)

