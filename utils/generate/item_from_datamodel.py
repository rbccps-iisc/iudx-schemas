import json

#modelName = input("Enter the datamodel.json name")
dataModelsDir = "../../data_models/"
baseSchemaDir = "../../base_schemas/"

# Where all the generated files get stored
project_root = "./workspace"

modelName = "../../data_models/power/feeder/pwr_feeder_slfeederShree_0.json"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def askAttr(attr):
    print
    pass



''' Data model '''
dataModel = {}
with open(modelName) as f :
    dataModel = json.loads(f.read())


''' Base data item field '''
baseDataItemSchema = {}
with open(dataModel["allOf"][0]["$ref"].replace("base_schemas",baseSchemaDir)
        .replace("#",""),"r") as f :
    baseDataItemSchema = json.loads(f.read())


''' Base schema '''
baseSchema = {}
with open(baseSchemaDir+baseDataItemSchema["allOf"][0]["$ref"].replace("#",""),"r") as f :
    baseSchema = json.loads(f.read())


''' Start creating item '''
baseItem = {}

print (bcolors.HEADER + "Warning: No active frommets remain. Continue?" 
      + bcolors.ENDC)
for attr in baseSchema["properties"] :
    baseItem[attr] = askAttr(attr)




