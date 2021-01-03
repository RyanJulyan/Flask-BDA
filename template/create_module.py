# Python 3

##########################
##########################
######## Imports #########
##########################
##########################
import os
import shutil
import re

##################################
##################################
######## Project Details #########
##################################
##################################

def getBool(prompt):
  while True:
    try:
      return {"true":True,"false":False}[input(prompt).lower()]
    except KeyError:
      print ("Invalid input please enter True or False!")

def getStringNum(prompt):
  while True:
    try:
        num = int(input(prompt))
        if(num < 1 or num > 256):
          return getStringNum("That's not a valid number between 1-256!\n"+prompt)
        return num
    except:
        print("That's not a valid number between 1-256!")

def getDataType(prompt):
  while True:
    try:
      return {
        "string":"String",
        "int":"Integer",
        "float":"Numeric(38, 19)",
        "numeric":"Numeric(38, 19)",
        "text":"Text",
        "date":"Date",
        "datetime":"DateTime",
        "boolean":"Boolean",
        "bigint":"BigInteger",
        "enum":"Enum",
        "json":"JSON",
        "largebinary":"LargeBinary"
      }[input(prompt).lower()]
    except KeyError:
      print ("Invalid data type")

def module():
  print("Module Name: ")
  while True:
    module = input()
    if(len(module) > 0):
      module = module.casefold()
      module = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', module)
      module = module.replace(" ", "_")
      return module
    else:  
      print("Invalid Module Name!")
      print("Please enter a valid module name:")

def getEnumParameters():
  parameters = []
  while True:
    field = input("Create new Parameter Value (type the string: 'STOP_CREATING_PARAMETERS' to exit): ")
    if(field == 'STOP_CREATING_PARAMETERS'):
      return parameters
    if(field in parameters):
      print("Parameter Value Already Exists!")
      print("Please enter a different parameter value!")
    elif(len(field) > 0):
      parameters.append(field)
    else:  
      print("Invalid Parameter Value!")
      print("Please enter a valid parameter value!")

def fields():
  fields = {}
  while True:
    print("Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): ")
    field = input()
    if(field == 'STOP_CREATING_FIELDS'):
      return fields
    if(field in fields):
      print("Field Name Already Exists!")
      print("Please enter a different field name!")
    elif(len(field) > 0):
      field = field.casefold()
      field = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', field)
      field = field.replace(" ", "_")
      dataType = getDataType("What datatype is " + field + """
        'String'
        'Int'
        'Float'
        'Numeric'
        'Text'
        'Date'
        'DateTime'
        'Boolean'
        'BigInt'
        'Enum'
        'JSON'
        'LargeBinary': """)
      if(dataType == 'String'):
        num = getStringNum("String Length (1-256):")
        dataType = "String(" + str(num) + ")"
      if(dataType == 'Enum'):
        parameters = getEnumParameters()
        dataType = "Enum(" + str((', '.join('"' + item + '"' for item in parameters))) + ")"
      nullable = getBool("Is " + field + " nullable ('True', 'False'): ")
      unique = getBool("Is " + field + " unique ('True', 'False'): ")
      default = input("Default value: ") or False
      fields[field] = {
        "dataType":dataType,
        "nullable":nullable,
        "unique":unique,
        "default":default
      }
    else:  
      print("Invalid Field Name!")
      print("Please enter a valid field name:")

# Prompt user 
module = module()
model = module.capitalize()
fields = fields()

# process user data
columns = '  \n'
feildNames = []
instanceNames = '    \n'
formDefinitions = '    \n'
instanceParams = ''

for key, value in fields.items():
  columns += "  {} = db.Column(db.{}, nullable={}, default={}, unique={})\n".format(key, value['dataType'],value['nullable'],value['default'],value['unique'])
  instanceNames += "    self.{} = {}\n".format(key, key)
  friendly_name = (key.capitalize()).replace('_', ' ')
  formDefinitions += "    {} = TextField('{}', [Required(message='Must provide a {}')])\n".format(key, friendly_name, friendly_name)
  feildNames.append(key)

instanceParams = str((', '.join( item for item in feildNames)))

################################################
################################################
######## Creating A Module / Component #########
################################################
################################################

########################################
########################################
######## Make Base Directories #########
########################################
########################################

def copytree(src, dst, renameFrom='',renameTo='', symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst.replace(renameFrom, renameTo))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst.replace(renameFrom, renameTo), item.replace(renameFrom, renameTo))
        if os.path.isdir(s):
            copytree(s, d, renameFrom, renameTo, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

copytree('create_module_template', 'app/', 'xyz', module)

############################
############################
######## mod_ Init #########
############################
############################

########################################################################
######## Copy App __init__.py for manage source -> destination #########
########################################################################

shutil.copy2('app/__init__.py', 'app/__init__.py~')

###############################################
######## manage source -> destination #########
###############################################

destination= open('app/__init__.py', "w" )
source = open('app/__init__.py~', "r" )

for line in source:
    
    destination.write( line )
    
    if "# import new xyz_module" in line:
        destination.write("# " + module + "\n" )
        destination.write("from app.mod_" + module + ".controllers import mod_public_" + module + " as " + module + "_public_module\n" )
        destination.write("from app.mod_" + module + ".controllers import mod_admin_" + module + " as " + module + "_admin_module\n" )
        destination.write("from app.mod_" + module + ".api_controllers import " + module.capitalize() + "ListResource, " + module.capitalize() + "Resource\n" )
    
    if "# register_blueprint new xyz_module" in line:
        destination.write("# " + module + "\n" )
        destination.write("app.register_blueprint(" + module + "_public_module)\n" )
        destination.write("app.register_blueprint(" + module + "_admin_module)\n" )
    
    if "# new xyz api resource routing" in line:
        destination.write("# " + module + "\n" )
        destination.write("api.add_resource(" + module.capitalize() + "ListResource, '/api/" + module + "')\n" )
        destination.write("api.add_resource(" + module.capitalize() + "Resource, '/api/" + module + "/<id>')\n" )

source.close()
destination.close()

################################
######## remove source #########
################################

os.remove('app/__init__.py~')

#############################################
#############################################
######## mod_  and template updates #########
#############################################
#############################################

def replaceTextBetweenTags(filePath, startBlockString, endBlockString, replacementString):

  searchExpressionString = startBlockString + '.*?' + endBlockString
  replacementString = f"""{startBlockString}
  {replacementString}
  {endBlockString}"""

  with open(filePath) as file :
    filedata = file.read()

  for line in filedata:
    filedata=re.sub(searchExpressionString, replacementString, filedata, flags=re.DOTALL)

  with open(filePath, 'w') as file:
    file.write(filedata)

  file.close()

def renameCustomizeFileVariables(src, renameFrom='',renameTo=''):
  for item in os.listdir(src):
        s = os.path.join(src, item)
        if os.path.isdir(s):
            renameCustomizeFileVariables(s, renameFrom, renameTo)
        else:
          ############################################################
          ######## Clean Required Values Between System Tags #########
          ############################################################
          
          if('forms.py' in s):
            replaceTextBetweenTags(s,'# start new form definitions','# end new form definitions','\n')
          if('models.py' in s):
            replaceTextBetweenTags(s,'# start new field definitions','# end new field definitions','\n')
            replaceTextBetweenTags(s,'# start new instance fields','# end new instance fields','\n')
          
          #############################################################
          ######## Copy temp for manage source -> destination #########
          #############################################################

          shutil.copy2(s, s+'~')

          ###############################################
          ######## manage source -> destination #########
          ###############################################

          destination= open(s, "w" )
          source = open(s+'~', "r" )
          
          for line in source:

            ###################################
            ######## Rename Variables #########
            ###################################
            
            if "def __init__" in line and 'models.py' in s:
              pass
            else:
              destination.write( ( line.replace(renameFrom, renameTo) ).replace(renameFrom.capitalize(), renameTo.capitalize()) )
            
            if "# start new form definitions" in line:
                destination.write(formDefinitions+"\n" )
            
            if "# start new field definitions" in line:
                destination.write(columns+"\n" )
            
            if "# start new instance fields" in line:
                destination.write(instanceNames+"\n" )
            
            
            if "def __init__" in line and 'models.py' in s:
                destination.write('  def __init__(self, ' + instanceParams + "): # ,example_field):\n" )
            
          source.close()
          destination.close()

          ################################
          ######## remove source #########
          ################################

          os.remove(s+'~')

renameCustomizeFileVariables('app/mod_'+module,'xyz',module)
renameCustomizeFileVariables('app/templates/'+module,'xyz',module)


