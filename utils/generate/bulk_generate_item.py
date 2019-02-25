import json
import datetime
import requests
import sys
import base64

''' Example item location '''
item_ex_name = "../../example_items/items/ex_aqm_item.json"

''' Bulk resources csv where the first row should be the attribute names which match the same names in the data model '''
bulk_csv = "../../../../../Downloads/ES_Static_Data_RBCCPS.csv"

''' Output dir where json files are stored '''
out_dir = "./workspace/output"

''' Temporary public data get link '''
getLink =  "https://pune.iudx.org.in/api/1.0.0/resource/latest/aqm-bosch-climo/XYZ"

attrDict = {}

def makeAttr(row):
    attrDict = {}
    attrDict["DEVICEID"] = row[0]
    attrDict["NAME"] = row[4]
    attrDict["resourceServerId"] = row[5]
    attrDict["address"] = row[1]
    attrDict["latitude"] = row[2]
    attrDict["longitude"] = row[3]
    return attrDict
        

with open(bulk_csv, "r") as f:
    bulk = f.readlines()
    attrs = [attr.strip("\n") for attr in bulk[0].split(",")]
    resources = [makeAttr([attr.strip("\n") for attr in row.split(",")]) for row in bulk[1:]]

with open(item_ex_name, "r") as f:
    item_ex = json.load(f)



''' Finds the key and adds the value from the csv for the same '''
def findKeyAndAdd(item, key, value):
    try:
        for attr in item:
            if isinstance(item[attr], list):
                for it in item[attr]:
                    findKeyAndAdd(it, key, value)
            if isinstance(item[attr], dict):
                findKeyAndAdd(item[attr], key, value)
                pass
            if(attr == key):
                item[attr] = value
    except Exception as e:
        pass
    return item


for resource in resources:
    for attr in attrs:
        item = findKeyAndAdd(item_ex, attr, resource[attr])
    item["__createdAt"] = datetime.datetime.now().isoformat('T')

    ''' Temporary get link. Make sure NAME exists in the csv file '''
    item["latestResourceData"] = getLink.replace("XYZ", resource["NAME"]).replace(" ","%20")

    with open(out_dir+"/"+resource[attr]+".json","w") as f:
        f.write(json.dumps(item, indent=4, sort_keys=True))
    item = {}
