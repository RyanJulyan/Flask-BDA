

###########
###########
# Imports #
###########
###########
import os
import shutil
import re
import secrets

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


def relationships(field):
    has_relationship = getBool("Does " + field + " have a Relationship with another Data Model? ('True', 'False'): ")
    while has_relationship:
        model = input("Which Model does the Field " + field + " have a Relationship with: ")
        if(len(model) > 0):
            model = model.lower()
            model = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', model)
            model = model.replace(" ", "_")
            return model
        else:
            print("Invalid model Name!")
            print("Please enter a valid model name:")
    return None

def module():
    print("Module Name: ")
    while True:
        module = input()
        if(len(module) > 0):
            module = module.lower()
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
            field = field.lower()
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
            relationship = relationships(field)
            default = input("Default value: ") or False
            fields[field] = {
                "dataType": dataType,
                "nullable": nullable,
                "unique": unique,
                "relationship": relationship,
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
formDefinitionsArr = []
newFormRequestDefinitionsArr = []
updateFormRequestDefinitionsArr = []
newApiRequestDefinitionsArr = []
updateApiRequestDefinitionsArr = []
newApiAggregateDefinitions = ''
argumentParserArr = []
instanceNames = ''
formDefinitions = ''
newFormRequestDefinitions = ''
updateFormRequestDefinitions = ''
newApiRequestDefinitions = ''
updateApiRequestDefinitions = ''
argumentParser = ''
instanceParams = ''
renderFields = ''
tableHeaders = ''
tableValues = ''

for key, value in fields.items():
    if value['relationship']:
        columns += "    {} = db.Column(db.{}, nullable={}, default={}, unique={}, db.ForeignKey('{}.id'))\n".format(key,
                                                                                                                    value['dataType'],
                                                                                                                    value['nullable'],
                                                                                                                    value['default'],
                                                                                                                    value['unique'],
                                                                                                                    value['relationship'])

        columns += "    {} = db.relationship('{}', backref = '{}', lazy='joined')\n".format(value['relationship'],
                                                                                            # secrets.token_urlsafe(3),
                                                                                            value['relationship'].capitalize(),
                                                                                            value['relationship'])

        columns += """
    @aggregated('{}_count', db.Column(db.Integer))
    def {}_count(self):
        return db.func.count('1')\n""".format(value['relationship'],
                                            value['relationship'])
    else:
        columns += "    {} = db.Column(db.{}, nullable={}, default={}, unique={})\n".format(key,
                                                                                    value['dataType'],
                                                                                    value['nullable'],
                                                                                    value['default'],
                                                                                    value['unique'])
    if "Numeric" in value['dataType'] or "Integer" in value['dataType']:
        newApiAggregateDefinitions += """
            func.count({}.{}).label('{}_count'),\n""".format(model,
                                            key,
                                            key)
        newApiAggregateDefinitions += """
            func.sum({}.{}).label('{}_sum'),\n""".format(model,
                                            key,
                                            key)
        newApiAggregateDefinitions += """
            func.avg({}.{}).label('{}_avg'),\n""".format(model,
                                            key,
                                            key)
        newApiAggregateDefinitions += """
            func.min({}.{}).label('{}_min'),\n""".format(model,
                                            key,
                                            key)
        newApiAggregateDefinitions += """
            func.max({}.{}).label('{}_max')""".format(model,
                                            key,
                                            key)

    instanceNames += "        self.{} = {}\n".format(key, key)
    friendly_name = (key.capitalize()).replace('_', ' ')
    if fields[key]['nullable']:
        formDefinitionsArr.append("\n    {} = TextField('{}')".format(key, key))
        argumentParserArr.append("\n    '{}': fields.String(description='The {} {}')".format(key, model, friendly_name))
    else:
        formDefinitionsArr.append("\n    {} = TextField('{}', [Required(message='Must provide a {}')])".format(key, key, friendly_name))
        argumentParserArr.append("\n    '{}': fields.String(required=True, description='The {} {}')".format(key, model, friendly_name))
    newFormRequestDefinitions += "        {}=request.form.get('{}')\n".format(key, key)
    updateApiRequestDefinitions += "        data.{} = api.payload['{}']\n".format(key, key)
    updateFormRequestDefinitions += "    data.{} = request.form.get('{}')\n".format(key, key)
    renderFields += """
                <div class="col-span-6 sm:col-span-3">
                  <label for="{}" class="block text-sm font-medium text-gray-700">{}</label>
                  <input type="text" name="{}" id="{}" placeholder="{}" autocomplete="{}" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                </div>
    """.format(key, friendly_name, key, key, friendly_name, key)
    tableHeaders += """
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {}
                    </th>
    """.format(friendly_name)
    tableValues += """
                        <td scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 capitalize tracking-wider">
                            {} value.{} {}
                        </td>
    """.format("{{", key, "}}")
    feildNames.append(key)
    newFormRequestDefinitionsArr.append("\n        {}=request.form.get('{}')".format(key, key))
    updateFormRequestDefinitionsArr.append("\n    data.{} = request.form.get('{}')".format(key, key))
    newApiRequestDefinitionsArr.append("\n            {}=api.payload['{}']".format(key, key))

instanceParams = str((', '.join(item for item in feildNames)))
formDefinitions = str((','.join(item for item in formDefinitionsArr)))
newFormRequestDefinitions = str((','.join(item for item in newFormRequestDefinitionsArr)))
updateFormRequestDefinitions = str((','.join(item for item in updateFormRequestDefinitionsArr)))
newApiRequestDefinitions = str((','.join(item for item in newApiRequestDefinitionsArr)))
argumentParser = str((','.join(item for item in argumentParserArr)))

newFormRequestDefinitions = newFormRequestDefinitions.lstrip('\n')
updateFormRequestDefinitions = updateFormRequestDefinitions.lstrip('\n')
newApiRequestDefinitions = newApiRequestDefinitions.lstrip('\n')
updateApiRequestDefinitions = updateApiRequestDefinitions.rstrip('\n')
argumentParser = argumentParser.lstrip('\n')
columns = columns.rstrip('\n')
instanceNames = instanceNames.rstrip('\n')
friendly_name = friendly_name.rstrip('\n')
formDefinitions = formDefinitions.lstrip('\n')
renderFields = renderFields.rstrip('\n')
tableHeaders = tableHeaders.rstrip('\n')
tableValues = tableValues.rstrip('\n')

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
    if "# register_blueprint new xyz_module" in line:
        destination.write("# " + module + "\n")
        destination.write("app.register_blueprint(" + module + "_public_module)\n")
        destination.write("app.register_blueprint(" + module + "_admin_module)\n")
    if "# new xyz api resources" in line:
        destination.write("# " + module + "\n")
        destination.write("from app.mod_" + module + ".api_controllers import ns as " + module.capitalize() + "_API  # noqa: E402\n")

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
                replaceTextBetweenTags(s, '# start new add_argument', '# end new add_argument', '    ', '')
                replaceTextBetweenTags(s, '# start update api_request feilds', '# end update api_request feilds', '        ', '')
                replaceTextBetweenTags(s, '# start new api_request feilds', '# end new api_request feilds', '            ', '')
                replaceTextBetweenTags(s, '# start new api_aggregate feilds', '# end new api_aggregate feilds', '            ', '')
            if('controllers.py' in s):
                replaceTextBetweenTags(s, '# start new request feilds', '# end new request feilds', '        ', '')
                replaceTextBetweenTags(s, '# start update request feilds', '# end update request feilds', '    ','')
            if('forms.py' in s):
                replaceTextBetweenTags(s, '# start new form definitions', '# end new form definitions', '    ', '')
            if('models.py' in s):
                replaceTextBetweenTags(s, '# start new field definitions', '# end new field definitions', '    ', '')
                replaceTextBetweenTags(s, '# start new instance fields', '# end new instance fields', '        ', '')
            if('index.html' in s):
                replaceTextBetweenTags(s, '<!-- start new table headers -->', '<!-- end new table headers -->', '                    ', '')
                replaceTextBetweenTags(s, '<!-- start new table values -->', '<!-- end new table values -->', '                        ', '')
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
                if "# start new api_request feilds" in line:
                    destination.write(newApiRequestDefinitions)
                if "# start update api_request feilds" in line:
                    destination.write(updateApiRequestDefinitions)
                if "# start new api_aggregate feilds" in line:
                    destination.write(newApiAggregateDefinitions)
                if "# start new form definitions" in line:
                    destination.write(formDefinitions)
                if "# start new field definitions" in line:
                    destination.write(columns)
                if "# start new instance fields" in line:
                    destination.write(instanceNames)
                if "<!-- start new render fields -->" in line:
                    destination.write(renderFields)
                if "<!-- start new table headers -->" in line:
                    destination.write(tableHeaders)
                if "<!-- start new table values -->" in line:
                    destination.write(tableValues)
                if "def __init__" in line and 'models.py' in s:
                    destination.write('    def __init__(self, ' + instanceParams + "):  # ,example_field):\n")
            source.close()
            destination.close()

            #################
            # remove source #
            #################

            os.remove(s+'~')


customizeFileVariables('app/mod_'+module, 'xyz', module)
customizeFileVariables('app/generated_config/models/'+module, 'xyz', module)
