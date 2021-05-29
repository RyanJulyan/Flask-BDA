

###########
###########
# Imports #
###########
###########
import os
import shutil
import re
import secrets
import json
import click

#######################
#######################
# Process Module JSON #
#######################
#######################

@click.command()
@click.option('--module', 
                    help='Name of module to create. It must have a JSON file to create from')
def cmd_create_module(module):
    """Generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input"""

    create_module(module)

def create_module(module):
    
    file = 'app/generated_config/models/'+ module + "/models.json"
    
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        json_module = data[module]
    
    model = json_module['model']
    fields = json_module['fields']

    # process user data
    module = model.lower()
    columns = ''
    feildNames = []
    formDefinitionsArr = []
    newFormRequestDefinitionsArr = []
    updateFormRequestDefinitionsArr = []
    newApiRequestDefinitionsArr = []
    updateApiRequestDefinitionsArr = []
    newApiAggregateDefinitions = ''
    newApiAggregateObjectDefinitions = ''
    argumentParserArr = []
    argumentAggParserArr = []
    instanceNames = ''
    formDefinitions = ''
    newFormRequestDefinitions = ''
    updateFormRequestDefinitions = ''
    newApiRequestDefinitions = ''
    updateApiRequestDefinitions = ''
    argumentParser = ''
    argumentAggParser = ''
    instanceParams = ''
    renderFields = ''
    renderUpdateFields = ''
    tableHeaders = ''
    tableValues = ''

    for key, value in fields.items():
        friendly_name = (key.capitalize()).replace('_', ' ')
        instanceNames += "        self.{} = {}\n".format(key, key)

        if value['relationship']:
            columns += "    {} = db.Column(db.{}, db.ForeignKey('{}.id'), nullable={}, default={}, unique={})\n".format(key,
                                                                                                                        value['dataType'],
                                                                                                                        value['relationship'],
                                                                                                                        value['nullable'],
                                                                                                                        value['default'],
                                                                                                                        value['unique'])

            columns += "    {} = db.relationship('{}', backref = '{}', remote_side='{}.id', lazy='joined')\n".format(value['relationship'],
                                                                                                # secrets.token_urlsafe(3),
                                                                                                value['relationship'].capitalize(),
                                                                                                value['relationship'],
                                                                                                value['relationship'].capitalize())

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
        
        newApiAggregateDefinitions += """
                func.count({}.{}).label('{}_count'),\n""".format(model,
                                            key,
                                            key)
        newApiAggregateObjectDefinitions += """
                "{}_count":data.{}_count,\n""".format(key,
                                            key)
        
        argumentAggParserArr.append("\n    '{}_count': fields.Integer(readonly=True, description='The {} {} count')".format(key, model, friendly_name))
        
        if "Numeric" in value['dataType'] or "Integer" in value['dataType']:
            newApiAggregateDefinitions += """
                func.sum({}.{}).label('{}_sum'),\n""".format(model,
                                                key,
                                                key)
            newApiAggregateObjectDefinitions += """
                "{}_sum":data.{}_sum,\n""".format(key,
                                                key)
            argumentAggParserArr.append("\n    '{}_sum': fields.Float(readonly=True, description='The {} {} sum')".format(key, model, friendly_name))

            newApiAggregateDefinitions += """
                func.avg({}.{}).label('{}_avg'),\n""".format(model,
                                                key,
                                                key)
            newApiAggregateObjectDefinitions += """
                "{}_avg":data.{}_avg,\n""".format(key,
                                                key)
            argumentAggParserArr.append("\n    '{}_avg': fields.Float(readonly=True, description='The {} {} avg')".format(key, model, friendly_name))

            newApiAggregateDefinitions += """
                func.min({}.{}).label('{}_min'),\n""".format(model,
                                                key,
                                                key)
            newApiAggregateObjectDefinitions += """
                "{}_min":data.{}_min,\n""".format(key,
                                                key)
            argumentAggParserArr.append("\n    '{}_min': fields.Float(readonly=True, description='The {} {} min')".format(key, model, friendly_name))

            newApiAggregateDefinitions += """
                func.max({}.{}).label('{}_max'),""".format(model,
                                                key,
                                                key)
            newApiAggregateObjectDefinitions += """
                "{}_max":data.{}_max,\n""".format(key,
                                                key)
            argumentAggParserArr.append("\n    '{}_max': fields.Float(readonly=True, description='The {} {} max')".format(key, model, friendly_name))

        if fields[key]['nullable']:
            formDefinitionsArr.append("\n    {} = TextField('{}')".format(key, key))
            if "Numeric" in value['dataType'] or "Integer" in value['dataType']:
                argumentParserArr.append("\n    '{}': fields.Float(description='The {} {}')".format(key, model, friendly_name))
            else:
                argumentParserArr.append("\n    '{}': fields.String(description='The {} {}')".format(key, model, friendly_name))
        else:
            formDefinitionsArr.append("\n    {} = TextField('{}', [Required(message='Must provide a {}')])".format(key, key, friendly_name))
            if "Numeric" in value['dataType'] or "Integer" in value['dataType']:
                argumentParserArr.append("\n    '{}': fields.Float(required=True, description='The {} {}')".format(key, model, friendly_name))
            else:
                argumentParserArr.append("\n    '{}': fields.String(required=True, description='The {} {}')".format(key, model, friendly_name))
        newFormRequestDefinitions += "        {} = request.form.get('{}')\n".format(key, key)
        updateApiRequestDefinitions += "        data.{} = api.payload['{}']\n".format(key, key)
        updateFormRequestDefinitions += "    data.{} = request.form.get('{}')\n".format(key, key)
        renderFields += """
                    <div class="form-group">
                        <label for="{}" class="col-sm-2 control-label">{}</label>

                        <div class="col-sm-10">
                            <input type="text" class="form-control" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                        </div>
                    </div>
        """.format(key, friendly_name, key, key, friendly_name, key)
        renderUpdateFields += """
                    <div class="form-group">
                        <label for="{}" class="col-sm-2 control-label">{}</label>

                        <div class="col-sm-10">
                            <input type="text" class="form-control" name="{}" id="{}" placeholder="{}" value="{}data.{}{}"  autocomplete="{}" >
                        </div>
                    </div>
        """.format(key, friendly_name, key, key, friendly_name, "{{", key, "}}", key)
        tableHeaders += """
                        <th>
                            {}
                        </th>
        """.format(friendly_name)
        tableValues += """
                            <td>
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
    argumentAggParser = str((','.join(item for item in argumentAggParserArr)))

    newFormRequestDefinitions = newFormRequestDefinitions.lstrip('\n')
    updateFormRequestDefinitions = updateFormRequestDefinitions.lstrip('\n')
    newApiRequestDefinitions = newApiRequestDefinitions.lstrip('\n')
    updateApiRequestDefinitions = updateApiRequestDefinitions.rstrip('\n')
    argumentParser = argumentParser.lstrip('\n')
    argumentAggParser = argumentAggParser.lstrip('\n')
    columns = columns.rstrip('\n')
    newApiAggregateDefinitions = newApiAggregateDefinitions.rstrip(',\n')
    newApiAggregateObjectDefinitions = newApiAggregateObjectDefinitions.rstrip(',\n')
    instanceNames = instanceNames.rstrip('\n')
    friendly_name = friendly_name.rstrip('\n')
    formDefinitions = formDefinitions.lstrip('\n')
    renderFields = renderFields.rstrip('\n')
    renderUpdateFields = renderUpdateFields.rstrip('\n')
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
                    if 'models.json' in s:
                        pass
                    else:
                        shutil.copy2(s, d)


    copytree('create_module_template/mod_xyz', 'app/mod_xyz', 'xyz', module)

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
                    replaceTextBetweenTags(s, '# start new api_aggregate_object feilds', '# end new api_aggregate_object feilds', '            ', '')
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
                    elif 'models.json' in s:
                        pass
                    else:
                        destination.write((line.replace(renameFrom, renameTo)).replace(renameFrom.capitalize(), renameTo.capitalize()))
                    if "# start new add_argument" in line:
                        destination.write(argumentParser)
                    if "# start new add_agg_argument" in line:
                        destination.write(argumentAggParser)
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
                    if "# start new api_aggregate_object feilds" in line:
                        destination.write(newApiAggregateObjectDefinitions)
                    if "# start new form definitions" in line:
                        destination.write(formDefinitions)
                    if "# start new field definitions" in line:
                        destination.write(columns)
                    if "# start new instance fields" in line:
                        destination.write(instanceNames)
                    if "<!-- start new render fields -->" in line:
                        destination.write(renderFields)
                    if "<!-- start new render_update fields -->" in line:
                        destination.write(renderUpdateFields)
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
    # customizeFileVariables('app/generated_config/models/'+module, 'xyz', module)

if __name__ == "__main__":
    cmd_create_module()