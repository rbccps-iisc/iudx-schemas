import json

#modelName = input("Enter the datamodel.json name")
modelName = "../data_models/environment/airQuality/env_aqm_climoPune_0.json"
project_root = ".."

baseDefs = "../"


dataModel = {}
with open(modelName) as f :
    dataModel = json.loads(f.read().replace("$project_root",project_root))

allOf = {}
with open(dataModel["allOf"][0]["$ref"].strip("#")) as f:
    allOf = json.loads(f.read())
print(allOf)
