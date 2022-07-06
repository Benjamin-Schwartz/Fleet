import requests
from base64 import b64encode
import json
import pandas as pd 
from dotenv import load_dotenv
import os



def configure():
    load_dotenv()



url = 'https://api.azuga.com/azuga-ws/v1/activity/list.json'

def request_trips():
    url = 'https://api.azuga.com/azuga-ws/v1/activity/list.json'
    headers = {'Authorization': 'Basic {}'.format(os.getenv('encoded_key'))}

    parameter = {
        'groupName': 'Default Group',
        'from': '07-05-2022 00:00:00',
        'to': '07-05-2022 12:55:00'
    }


    response = requests.get(url, headers=headers, params = parameter)

    return json.loads(response.text)


def main():

    configure()

    json_dict= request_trips()

    df = pd.DataFrame(json_dict['activityResponseVO']['activityReport'])

    df.to_csv("test.csv", index = False)

main()


