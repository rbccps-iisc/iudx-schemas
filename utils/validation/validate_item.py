import os
import json
import jsonschema
import sys

cwd = os.getcwd()
base_dir_abs_path = cwd+'/'

if (len(sys.argv[1:])==0):
  print (("Usage: python validate_item.py rel-path-to-item"))
  exit()
else:
  data_path = os.path.join(base_dir_abs_path, sys.argv[1])


# Your data
#data_path = os.path.join(base_dir_abs_path, sys.argv[1])
with open(data_path) as data_object:
    data = json.load(data_object)

bschPath = data['refBaseSchema']
dMPath = data['refDataModel']
rel_bschPath = 'base_schemas' + bschPath.split('base_schemas')[-1]
rel_bdMPath = 'data_models' + dMPath.split('data_models')[-1]
#print bschPath
#print dMPath


item_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "allOf": [
   {"$ref": bschPath},
   {"$ref": dMPath}
  ]
}
#print item_schema['allOf'][0]['$ref']
#print json.dumps(item_schema)

# Note that the second parameter does nothing.
#resolver = jsonschema.RefResolver('file://' + root_dir_path + path_for_schema, None)

# This will find the correct validator and instantiate it using the resolver.
# Requires that your schema a line like this: "$schema": "http://json-schema.org/draft-04/schema#"
try:
 #jsonschema.validate(data, schema, resolver=resolver)
 jsonschema.validate(data, item_schema)

except jsonschema.exceptions.ValidationError as errV:
 print ("Validation Error Occured")
 #print errV
 #v = jsonschema.Draft7Validator(schema, types=(), resolver=resolver, format_checker=None)
 v = jsonschema.Draft7Validator(item_schema, types=(), format_checker=None)
 #for error in sorted(v.iter_errors(data), key=str):
 #    print(error.message)
 errors = sorted(v.iter_errors(data), key=lambda e: e.path)
 for error in errors:
     print (error.message)

except jsonschema.exceptions.SchemaError as errS:
 print ("Schema Error Occured")
 print (errS.message)
