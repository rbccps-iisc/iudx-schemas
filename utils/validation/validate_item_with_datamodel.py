import os
import json
import jsonschema
import sys

cwd = os.getcwd()
#base_dir_abs_path = cwd+'/'+sys.argv[3]
base_dir_abs_path = cwd+'/.'

if (len(sys.argv[1:])==0):
  print "Usage: python jsonschema_val.py rel-path-to-item [rel-path-to-root-dir]"
  exit()
elif (len(sys.argv[1:])==1):
  root_dir = base_dir_abs_path
else:
  root_dir = os.path.join(base_dir_abs_path, sys.argv[2]) + '/.'
  #schema_file = os.path.join(base_dir_abs_path, sys.argv[2])

# Your data
data_path = os.path.join(base_dir_abs_path, sys.argv[1])
with open(data_path) as data_object:
    data = json.load(data_object)

filename = data['refDataModel']
fname = filename.split("master/")[-1]

schema_file= os.path.join(root_dir, fname)

#schema_file= os.path.join(root_dir, data['refDataModel'])
print schema_file

with open(schema_file) as file_object:
    schema = json.load(file_object)


# Note that the second parameter does nothing.
#resolver = jsonschema.RefResolver('file://' + base_dir_abs_path + '/', None)
resolver = jsonschema.RefResolver('file://' + root_dir + '/.', None)

# This will find the correct validator and instantiate it using the resolver.
# Requires that your schema a line like this: "$schema": "http://json-schema.org/draft-04/schema#"
try:
 jsonschema.validate(data, schema, resolver=resolver)

except jsonschema.exceptions.ValidationError as errV:
 print "Validation Error Occured"
 #print errV
 v = jsonschema.Draft7Validator(schema, types=(), resolver=resolver, format_checker=None)
 #for error in sorted(v.iter_errors(data), key=str):
 #    print(error.message)
 errors = sorted(v.iter_errors(data), key=lambda e: e.path)
 for error in errors:
     print error.message

except jsonschema.exceptions.SchemaError as errS:
 print "Schema Error Occured"
 print errS.message
