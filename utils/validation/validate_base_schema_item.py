import os
import json
import jsonschema
import sys
import wget

cwd = os.getcwd()
base_dir_abs_path = cwd+'/'

if (len(sys.argv[1:])==0):
  print "Usage: python jsonschema_val.py rel-path-to-item abs-rel-switch [rel-path-to-root-dir]"
  exit()
elif (len(sys.argv[1:])==1):
  print "Usage: python jsonschema_val.py rel-path-to-item abs-rel-switch [rel-path-to-root-dir]"
  exit()
elif (len(sys.argv[1:])==2):
  root_dir_path = cwd+'/'
else:
  root_dir_path = os.path.join(base_dir_abs_path, sys.argv[3])+'/'

# Your data
data_path = os.path.join(base_dir_abs_path, sys.argv[1])
with open(data_path) as data_object:
    data = json.load(data_object)


#If required to run the validation script using absolute path
if (sys.argv[2] == "0"):
   schema_url = data['refBaseSchema']
   schema_name = data['refBaseSchema'].split('/')[-1]

   print "\n-------------------------------------------------------------------------------------------\n"
   print "Json item     :"+ sys.argv[1] + '\n'
   print "Schema File   :" + schema_url
   print "\n-------------------------------------------------------------------------------------------\n"

   with open(wget.download(schema_url),'r') as fobj:
      schema = json.load(fobj)

   os.remove(cwd+'/'+schema_name)
   print "\n"

   try:
      jsonschema.validate(data, schema)
   
   except jsonschema.exceptions.ValidationError as errV:
      print "Validation Error Occured"
      v = jsonschema.Draft7Validator(schema, types=(), format_checker=None)
      errors = sorted(v.iter_errors(data), key=lambda e: e.path)
      for error in errors:
          print error.message
   
   except jsonschema.exceptions.SchemaError as errS:
      print "Schema Error Occured"
      print errS.message


else :
   #relative_schema_file_path = data['refBaseSchema'].split('/')[-3] + '/'+data['refBaseSchema'].split('/')[-2]+'/'+data['refBaseSchema'].split('/')[-1]
   #File link
   relative_schema_file_path = data['refBaseSchema']
   #schema_path = relative_schema_file_path
   #schema_file = os.path.join(root_dir_path + schema_path)
   schema_file = relative_schema_file_path
   print "-------------------------------------------------------------------------------------------\n"
   print "Json item     :"+ sys.argv[1] + '\n'
   print "Schema File   :" + relative_schema_file_path
   print "\n-------------------------------------------------------------------------------------------\n"

   with open(schema_file) as file_object:
       schema = json.load(file_object)


   # Note that the second parameter does nothing.
   # Each external file reference should have the full path
   resolver = jsonschema.RefResolver('file://', None)
   
   try:
      jsonschema.validate(data, schema, resolver=resolver)
   
   except jsonschema.exceptions.ValidationError as errV:
      print "Validation Error Occured"
      #print errV
      v = jsonschema.Draft7Validator(schema, types=(), resolver=resolver, format_checker=None)
      errors = sorted(v.iter_errors(data), key=lambda e: e.path)
      for error in errors:
          print error.message
   
   except jsonschema.exceptions.SchemaError as errS:
      print "Schema Error Occured"
      print errS.message
