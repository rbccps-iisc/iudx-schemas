'''
    Uploade files en-bulk to IUDX
'''
import json
import datetime
import requests
import sys
import base64
import os

cat_link = "https://catalogue.iudx.org.in/cat/items"

''' Input directory where all the jsons are stored '''
in_dir = "./workspace/output/"

''' Args '''
identity = sys.argv[1]
password = sys.argv[2]
authString = base64.b64encode(identity+":"+password )
headers = {"Authorization":"Basic " + authString, 'skip_validation':"true"}

for filename in os.listdir(in_dir):
    with open(in_dir+filename,"r") as f:
        r = requests.post(cat_link, 
                data = json.dumps(json.load(f)), headers=headers, verify=False)
        print(r.text)
