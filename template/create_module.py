

###########
###########
# Imports #
###########
###########
import os
import shutil
import re

###################
###################
# Project Details #
###################
###################


def getBool(prompt):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter True or False!")


def getStringNum(prompt):
    while True:
        try:
            num = int(input(prompt))
            if(num < 1 or num > 256):
                return getStringNum("That's not a valid number between 1-256!\n"+prompt)
            return num
        except KeyError:
            print("That's not a valid number between 1-256!")


def getDataType(prompt):
    while True:
        try:
            return {
                "string": "String",
                "int": "Integer",
                "float": "Numeric(38, 19)",
                "numeric": "Numeric(38, 19)",
                "text": "Text",
                "date": "Date",
                "datetime": "DateTime",
                "boolean": "Boolean",
                "bigint": "BigInteger",
                "enum":  "Enum",
                "json": "JSON",
                "largebinary": "LargeBinary"
            }[input(prompt).lower()]
        except KeyError:
            print("Invalid data type")


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
    print("Create new data model for your module " + module + ": ")
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
            Choose one of the following options
            ('String'
             ,'Int'
             ,'Float'
             ,'Numeric'
             ,'Text'
             ,'Date'
             ,'DateTime'
             ,'Boolean'
             ,'BigInt'
             ,'Enum'
             ,'JSON'
             ,'LargeBinary'): """)
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
                "dataType": dataType,
                "nullable": nullable,
                "unique": unique,
                "default": default
            }
        else:
            print("Invalid Field Name!")
            print("Please enter a valid field name:")


# Prompt user
module = module()
model = module.capitalize()
fields = fields()

# process user data
columns = ''
feildNames = []
instanceNames = ''
formDefinitions = ''
newFormRequestDefinitions = ''
updateFormRequestDefinitions = ''
newApiRequestDefinitions = ''
updateApiRequestDefinitions = ''
argumentParser = ''
instanceParams = ''
renderFields = ''

for key, value in fields.items():
    columns += "    {} = db.Column(db.{}, nullable={}, default={}, unique={})\n".format(key,
                                                                                    value['dataType'],
                                                                                    value['nullable'],
                                                                                    value['default'],
                                                                                    value['unique'])
    instanceNames += "        self.{} = {}\n".format(key, key)
    friendly_name = (key.capitalize()).replace('_', ' ')
    if fields[key]['nullable']:
        formDefinitions += "    {} = TextField('{}')\n".format(key, key)
        argumentParser += "parser.add_argument('{}', help='{} of {}')\n".format(key, key, friendly_name)
    else:
        formDefinitions += "    {} = TextField('{}', [Required(message='Must provide a {}')])\n".format(key, key, friendly_name)
        argumentParser += "parser.add_argument('{}', required=True, help='{} of {}')\n".format(key, key, friendly_name)
    newApiRequestDefinitions += "            {}=args['{}']\n".format(key, key)
    newFormRequestDefinitions += "        {}=request.form.get('{}')\n".format(key, key)
    updateApiRequestDefinitions += "    data.{} = args['{}']\n".format(key, key)
    updateFormRequestDefinitions += "    data.{} = request.form.get('{}')\n".format(key, key)
    renderFields += """
                <div class="col-span-6 sm:col-span-3">
                  <label for="{}" class="block text-sm font-medium text-gray-700">{}</label>
                  {} render_field(form.{}, autocomplete="{}", placeholder="{}") {}
                  <input type="text" name="{}" id="last_name" autocomplete="{}" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                </div>
    """.format(key, friendly_name,"{{", key, key, friendly_name, "}}", key, key)
    feildNames.append(key)

instanceParams = str((', '.join(item for item in feildNames)))

newFormRequestDefinitions = newFormRequestDefinitions.rstrip('\n')
updateFormRequestDefinitions = updateFormRequestDefinitions.rstrip('\n')
newApiRequestDefinitions = newApiRequestDefinitions.rstrip('\n')
argumentParser = argumentParser.rstrip('\n')
columns = columns.rstrip('\n')
instanceNames = instanceNames.rstrip('\n')
friendly_name = friendly_name.rstrip('\n')
formDefinitions = formDefinitions.rstrip('\n')
renderFields = renderFields.rstrip('\n')

#############
#############
# mod_ Init #
#############
#############

#########################################################
# Copy App __init__.py for manage source -> destination #
#########################################################

shutil.copy2('app/__init__.py', 'app/__init__.py~')

################################
# manage source -> destination #
################################

source = open('app/__init__.py~', "r")
destination = open('app/__init__.py', "w")

for line in source:
    destination.write(line)
    if "# import new xyz_module" in line:
        destination.write("# " + module + "\n")
        destination.write("from app.mod_" + module + ".controllers import mod_public_" + module + " as " + module + "_public_module  # noqa: E402\n")
        destination.write("from app.mod_" + module + ".controllers import mod_admin_" + module + " as " + module + "_admin_module  # noqa: E402\n")
        destination.write("from app.mod_" + module + ".api_controllers import " + module.capitalize() + "ListResource, " + module.capitalize() + "Resource  # noqa: E402\n")
    if "# register_blueprint new xyz_module" in line:
        destination.write("# " + module + "\n")
        destination.write("app.register_blueprint(" + module + "_public_module)\n")
        destination.write("app.register_blueprint(" + module + "_admin_module)\n")
    if "# new xyz api resource routing" in line:
        destination.write("# " + module + "\n")
        destination.write("api.add_resource(" + module.capitalize() + "ListResource, '/api/" + module + "')\n")
        destination.write("api.add_resource(" + module.capitalize() + "Resource, '/api/" + module + "/<id>')\n")

source.close()
destination.close()

#################
# remove source #
#################

os.remove('app/__init__.py~')

#################################
#################################
# Creating A Module / Component #
#################################
#####################x###########

#########################
#########################
# Make Base Directories #
#########################
#########################


def copytree(src, dst, renameFrom='', renameTo='', symlinks=False, ignore=None):
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

##############################
##############################
# mod_  and template updates #
##############################
##############################


def replaceTextBetweenTags(filePath, startBlockString, endBlockString, indentPadding, replacementString):
    searchExpressionString = startBlockString + '.*?' + endBlockString
    replacementString = f"""{startBlockString}\n{replacementString}\n{indentPadding}{endBlockString}"""

    with open(filePath) as file:
        filedata = file.read()

    for line in filedata:
        filedata = re.sub(searchExpressionString, replacementString, filedata, flags=re.DOTALL)

    with open(filePath, 'w') as file:
        file.write(filedata)

    file.close()


def customizeFileVariables(src, renameFrom='', renameTo=''):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if os.path.isdir(s):
            customizeFileVariables(s, renameFrom, renameTo)
        else:
            #############################################
            # Clean Required Values Between System Tags #
            #############################################
            if('api_controllers.py' in s):
                replaceTextBetweenTags(s, '# start new add_argument', '# end new add_argument', '', '')
                replaceTextBetweenTags(s, '# start update api_request feilds', '# end update api_request feilds', '        ', '')
                replaceTextBetweenTags(s, '# start new api_request feilds', '# end new api_request feilds', '            ', '')
            if('controllers.py' in s):
                replaceTextBetweenTags(s, '# start new request feilds', '# end new request feilds', '        ', '')
                replaceTextBetweenTags(s, '# start update request feilds', '# end update request feilds', '    ','')
            if('forms.py' in s):
                replaceTextBetweenTags(s, '# start new form definitions', '# end new form definitions', '    ', '')
            if('models.py' in s):
                replaceTextBetweenTags(s, '# start new field definitions', '# end new field definitions', '    ', '')
                replaceTextBetweenTags(s, '# start new instance fields', '# end new instance fields', '        ', '')
            if('create.html' in s):
                replaceTextBetweenTags(s, '<!-- start new render fields -->', '<!-- end new render fields -->', '                ', '')
            ##############################################
            # Copy temp for manage source -> destination #
            ##############################################
            shutil.copy2(s, s+'~')
            ################################
            # manage source -> destination #
            ################################
            source = open(s+'~', "r")
            destination = open(s, "w")
            for line in source:
                ####################
                # Rename Variables #
                ####################
                if "def __init__" in line and 'models.py' in s:
                    pass
                elif "fields" in line and 'models.json' in s:
                    destination.write('        "fields": ' + str(fields).replace("'",'"')+'\n    }\n')
                else:
                    destination.write((line.replace(renameFrom, renameTo)).replace(renameFrom.capitalize(), renameTo.capitalize()))
                if "# start new add_argument" in line:
                    destination.write(argumentParser)
                if "# start new request feilds" in line:
                    destination.write(newFormRequestDefinitions)
                if "# start update request feilds" in line:
                    destination.write(updateFormRequestDefinitions)
                if "# start new form definitions" in line:
                    destination.write(formDefinitions)
                if "# start new field definitions" in line:
                    destination.write(columns)
                if "# start new instance fields" in line:
                    destination.write(instanceNames)
                if "<!-- start new render fields -->" in line:
                    destination.write(renderFields)
                if "def __init__" in line and 'models.py' in s:
                    destination.write('    def __init__(self, ' + instanceParams + "):  # ,example_field):\n")
            source.close()
            destination.close()

            #################
            # remove source #
            #################

            os.remove(s+'~')


customizeFileVariables('app/mod_'+module, 'xyz', module)
customizeFileVariables('app/templates/'+module, 'xyz', module)
customizeFileVariables('app/generated_config/models/'+module, 'xyz', module)
