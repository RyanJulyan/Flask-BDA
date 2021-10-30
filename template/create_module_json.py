

###########
###########
# Imports #
###########
###########
import os
import shutil
import re
import json
import click
from create_module import create_module
from create_all_models_json import create_models_json

###################
###################
# Project Details #
###################
###################

@click.command()
@click.option('--module', 
                    help='Name of module to create. It must have a JSON file to create from')
# @click.pass_context
def cmd_create_module_json(module):
    """Generate module JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input. This JSON file is used to create a module"""

    create_module_json(module)

def create_module_json(module_name):
    """Generate module JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input. This JSON file is used to create a module"""

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


    def setDataTypeLower(prompt):
        while True:
            try:
                return {
                    "string": "string",
                    "int": "int",
                    "float": "float",
                    "numeric": "numeric",
                    "text": "text",
                    "date": "date",
                    "datetime": "datetime",
                    "boolean": "boolean",
                    "bigint": "bigint",
                    "enum":  "enum",
                    "json": "json",
                    "relationship": "relationship",
                    "largebinary": "largebinary",
                    "password": "password",
                    "color": "color",
                    "email": "email",
                    "range": "range",
                    "file": "file"
                }[input(prompt).lower()]
            except KeyError:
                print("Invalid data type")


    def getDataType(DataTypeLower):
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
                # "bigint": "BigInteger",
                "bigint": "Integer",
                # "enum":  "Enum",
                "enum":  "String",
                # "json": "JSON",
                "largebinary": "LargeBinary",
                "json": "Text",
                "relationship": "Integer",
                # "largebinary": "Text",
                "password": "String(256)",
                "color": "String(10)",
                "email": "String(256)",
                "range": "Numeric(38, 19)",
                "file": "Text"
            }[DataTypeLower]
        except KeyError:
            print("Invalid data type")


    def getGrapheneDataType(DataTypeLower):
        try:
            return {
                "string": "String(required=True)",
                "int": "Int(required=True)",
                "float": "Decimal(required=True)",
                "numeric": "Decimal(required=True)",
                "text": "String(required=True)",
                "date": "Date(required=True)",
                "datetime": "DateTime(required=True)",
                "boolean": "Boolean(required=True)",
                "bigint": "Int(required=True)",
                "enum":  "String(required=True)",
                "json": "JSONString(required=True)",
                "relationship": "Int(required=True)",
                "largebinary": "String(required=True)",
                "password": "String(required=True)",
                "color": "String(required=True)",
                "email": "String(required=True)",
                "range": "Decimal(required=True)",
                "file": "String(required=True)"
            }[DataTypeLower]
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


    def create_name(prompt):
        name = input(prompt)
        while True:
            if(len(name) > 0):
                name = name.lower()
                name = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', name)
                name = name.replace(" ", "_")
                return name
            else:
                print("Invalid Name!")
                name = input("Please enter a valid name: ")


    def create_module_name(module_name):
        module = module_name
        while True:
            if(len(module) > 0):
                module = module.lower()
                module = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', module)
                module = module.replace(" ", "_")
                return module
            else:
                print("Invalid Name!")
                module = input("Please enter a valid name: ")


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
                orgDataType = setDataTypeLower("What datatype is " + field + """
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
                ,'Relationship'
                ,'LargeBinary'
                ,'password'
                ,'color'
                ,'email'
                ,'range'
                ,'file'): """)
                dataType = orgDataType
                grapheneDataType = getGrapheneDataType(orgDataType)
                dataType = getDataType(orgDataType)
                if(dataType == 'String'):
                    num = getStringNum("String Length (1-256):")
                    dataType = "String(" + str(num) + ")"
                if(dataType == 'Enum'):
                    parameters = getEnumParameters()
                    dataType = "Enum(" + str((', '.join('"' + item + '"' for item in parameters))) + ")"
                nullable = getBool("Is " + field + " nullable ('True', 'False'): ")
                grapheneDataType = grapheneDataType.replace('True', str(not nullable))
                unique = getBool("Is " + field + " unique ('True', 'False'): ")
                index = getBool("Does " + field + " have an index ('True', 'False'): ")
                relationship = relationships(field)
                relationship_display_value = None
                if relationship:
                    relationship_display_value = create_name("Which Field Name from " + relationship + " do you want to see on the front end?")
                default = input("Default value: ") or False
                fields[field] = {
                    "dataTypeLower": orgDataType,
                    "dataType": dataType,
                    "grapheneDataType": grapheneDataType,
                    "nullable": nullable,
                    "unique": unique,
                    "index": index,
                    "relationship": relationship,
                    "relationship_display_value": relationship_display_value,
                    "default": default
                }
            else:
                print("Invalid Field Name!")
                print("Please enter a valid field name:")


    # Prompt user
    module = create_module_name(module_name)
    model = module.capitalize()
    fields = fields()

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


    copytree('create_module_template/generated_config', 'app/generated_config/', 'xyz', module)

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
                    if "fields" in line and 'models.json' in s:
                        destination.write('        "fields": ' + str(json.dumps(fields, indent=12, sort_keys=True)).replace("'",'"')+'\n')
                    else:
                        destination.write((line.replace(renameFrom, renameTo)).replace(renameFrom.capitalize(), renameTo.capitalize()))
                source.close()
                destination.close()

                #################
                # remove source #
                #################

                os.remove(s+'~')


    customizeFileVariables('app/generated_config/models/'+module, 'xyz', module)


    create_module_from_model = getBool("Create module logic from Data Model? ('True', 'False'): ")

    if create_module_from_model:

        # file = 'app/generated_config/models/'+module + "/models.json"
        # with open(file, 'r') as json_file:
        #     data = json.load(json_file)
        #     create_module(data[module])
        create_module(module)

    create_models_json()


if __name__ == "__main__":
    cmd_create_module_json()