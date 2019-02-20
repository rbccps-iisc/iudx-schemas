'''
    Creates a datamodel given CSV rows.
    Requires to be executed in this directory
    Directory with name of this datamodel is created in example_items/
        and .json is stored within it
'''
import json
import os


attrList = []

''' Open schema template '''
with open("./templates/data_model_template.json","r") as f:
    try:
        template = json.loads(f.read())
    except Exception as e:
        print(e)
        exit()


''' Open data dump csv '''
with open("../example_items/ES_Data.csv","r") as f:
    try:
        row = f.readline().strip("\n")
    except Exception as e:
        print(e)
        exit()

attTemplateDict = {"1":"./templates/data_attribute_string_template.json",
                   "2":"./templates/data_attribute_number_template.json",
                   "3":"./templates/data_attribute_integer_template.json",
                   "4":"./templates/data_attribute_enum_template.json",
                   "5":"./templates/data_attribute_array_template.json"
                   }

def make_attribute(name):
    print("What's the type of data")
    typ = input("\t1) string \n\t2) integer \n\t3) number \n\t4) enum\n\t5)array \n")
    attrTypeString = attTemplateDict[typ]
    attrDict = {}
    dscr = input("Enter any description of this attribute \t")
    with open(attrTypeString,"r") as f:
        attrDict = json.loads(f.read().replace("$attr",name))
        attrDict[name]["description"] = dscr
    if typ == "1":
        pass
    if typ == "2" or typ == "3":
        unts = input("What are the units of this attribute \t")
        mi = float(input("What's the minimum value this attribute might describe \t"))
        mx = float(input("What's the maximum value this attribute might describe \t"))
        attrDict[name]["units"] = unts
        attrDict[name]["minimum"] = mi
        attrDict[name]["maximum"] = mx
    if typ == "4":
        enm = list(input("Enter the enums as comma seperated strings \t").split(','))
        attrDict[name]["enum"] = enm
    if typ == "5":
        tp = list(input("Enter the type of array \t").split(','))
        attrDict[name]["items"]["type"] = tp
    return attrDict

def ask(column):

    attr = {}
    print("\n\n---------------- \n\n")
    print("Attribute Name = \t" + column)
    attr = make_attribute(column)
    template["properties"].update(attr)


nm = input("Enter the name of this data model \t")
dirName = "../example_items/" + nm.strip(".json")
os.mkdir(dirName)
dscr = input("What does this data model describe? \t")
template["name"] = nm

for col in row.split(","):
    try:
        ask(col)
    except Exception as e:
        print(e)


req = input("Enter the required fields as comma seperated nubers \n").split(',')
template["required"] = req

with open(dirName+"/"+nm,"w") as f:
    f.write(json.dumps(template, indent=4, sort_keys=True))

