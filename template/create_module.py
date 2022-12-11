

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


    def getHtmlCreateInput(DataTypeLower,key, friendly_name, relationship, relationship_display_value):
        try:
            return {
                'string':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'int':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'float':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'numeric':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'text':"""
                                    <div class="col-sm-10">
                                        <textarea class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >{}form.{}.data{}</textarea>
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key, "{{", key, "}}"),
                'date':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control daterangepicker_single {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'datetime':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control daterangepicker_single {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'boolean':"""
                                    <div class="col-sm-10">
                                        <input type="checkbox" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" {}% if form.{}.data == 'True' %{} checked="true" {}% endif %{} value="True" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{", key, "}", "{", "}", key),
                'bigint':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'enum':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'json':"""
                                    <script>
                                        generic_key = 'generic_key_value';
                                        key_value = '';
                                        localStorage.setItem(generic_key, key_value);
                                    </script>
                                    <div class="col-sm-10" id="key_value_inputs">

                                    </div>
                                    <div class="col-sm-12">
                                        &nbsp;
                                    </div>
                                    <div class="col-sm-10">
                                        <input type="hidden" id="key_value" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" placeholder="{}" autocomplete="{}">
                                    </div>
                                    <div class="col-sm-2">
                                        <button type="button" class="form-control btn btn-block btn-primary" name="add_key_value" id="add_key_value" ><i class="fa fa-plus"></i></button>
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, friendly_name.replace('_'," "), key),
                'relationship':"""
                                    <div class="col-sm-10">
                                        <select class="select2 form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                            <option aria-readonly="true" readonly="true" disabled="true" selected="true">Choose {}</option>
                                            {}% for obj in {} %{}
                                                <option value="{}obj.id{}">{}obj.{}{}</option>
                                            {}% endfor %{}
                                        </select>
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key, relationship, "{", relationship, "}", "{{", "}}", "{{", relationship_display_value, "}}", "{", "}"),
                'largebinary':"""
                                    <div class="col-sm-10">
                                        <textarea class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >{}form.{}.data{}</textarea>
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key, "{{", key, "}}"),
                'password':"""
                                    <div class="col-sm-10">
                                        <input type="password" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key),
                'color':"""
                                    <div class="col-sm-10">
                                        <input type="color" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'email':"""
                                    <div class="col-sm-10">
                                        <input type="email" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'range':"""
                                    <div class="col-sm-10">
                                        <input type="range" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" value="{}form.{}.data{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", "{{", key, "}}", key, key, friendly_name.replace('_'," "), key),
                'file':"""
                                    <div class="col-sm-10">
                                        <input type="file" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key)
            }[DataTypeLower]
        except KeyError:
            print("Invalid data type")
    

    def getHtmlUpdateInput(DataTypeLower,key, friendly_name, relationship, relationship_display_value):
        try:
            return {
                'string':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'int':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'float':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'numeric':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'text':"""
                                    <div class="col-sm-10">
                                        <textarea class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >{}form.{}.data{}</textarea>
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key, "{{", key, "}}"),
                'date':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control daterangepicker_single {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'datetime':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control daterangepicker_single {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'boolean':"""
                                    <div class="col-sm-10">
                                        <input type="checkbox" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" {}% if form.{}.data == 'True' %{} checked="true" {}% endif %{} value="True" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{", key, "}", "{", "}", key),
                'bigint':"""
                                    <div class="col-sm-10">
                                        <input type="number" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'enum':"""
                                    <div class="col-sm-10">
                                        <input type="text" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'json':"""
                                    <script>
                                        generic_key = 'generic_key_value';
                                        key_value = JSON.stringify({}data.{}{}|safe}});
                                        localStorage.setItem(generic_key, key_value);
                                    </script>
                                    <div class="col-sm-10" id="key_value_inputs">

                                    </div>
                                    <div class="col-sm-12">
                                        &nbsp;
                                    </div>
                                    <div class="col-sm-10">
                                        <input type="hidden" id="key_value" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}">
                                    </div>
                                    <div class="col-sm-2">
                                        <button type="button" class="form-control btn btn-block btn-primary" name="add_key_value" id="add_key_value" ><i class="fa fa-plus"></i></button>
                                    </div>""".format("{{", key, "}}", "{", key, "}", "{", "}", key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'relationship':"""
                                    <div class="col-sm-10">
                                        <select class="select2 form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" autocomplete="{}" >
                                            <option aria-readonly="true" readonly="true" disabled="true">Choose {}</option>
                                            {}% for obj in {} %{}
                                                <option value="{}obj.id{}" {}% if data.{} == obj.id %{} selected="true"{}% endif %{}>{}obj.{}{}</option>
                                            {}% endfor %{}
                                        </select>
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), key, relationship, "{", relationship, "}", "{{", "}}", "{", key, "}", "{", "}", "{{", relationship_display_value, "}}", "{", "}"),
                'largebinary':"""
                                    <div class="col-sm-10">
                                        <textarea class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'password':"""
                                    <div class="col-sm-10">
                                        <input type="password" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'color':"""
                                    <div class="col-sm-10">
                                        <input type="color" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'email':"""
                                    <div class="col-sm-10">
                                        <input type="email" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'range':"""
                                    <div class="col-sm-10">
                                        <input type="range" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key),
                'file':"""
                                    <div class="col-sm-10">
                                        <input type="file" class="form-control {}% if form.{}.errors %{} is-invalid {}% endif %{}" name="{}" id="{}" placeholder="{}" value="{}form.{}.data{}" autocomplete="{}" >
                                    </div>""".format("{", key, "}", "{", "}", key, key, friendly_name.replace('_'," "), "{{", key, "}}", key)
            }[DataTypeLower]
        except KeyError:
            print("Invalid data type")
    
    
    file = 'app/generated_config/models/'+ module + "/models.json"
    
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        json_module = data[module]
    
    model = json_module['model']
    fields = json_module['fields']

    # process user data
    module = model.lower()
    columns = ''
    grapheneColumns = ''
    feildNames = []
    formDefinitionsArr = []
    newBrokerDataDefinitionsArr = []
    newFormRequestDefinitionsArr = []
    updateFormRequestDefinitionsArr = []
    newApiRequestDefinitionsArr = []
    updateApiRequestDefinitionsArr = []
    newApiAggregateDefinitions = ''
    newApiAggregateObjectDefinitions = ''
    argumentParserArr = []
    argumentAggParserArr = []
    contextDataArr = []
    instanceNames = ''
    instanceDictNames = ''
    formDefinitions = ''
    newBrokerDataDefinitions = ''
    newFormRequestDefinitions = ''
    updateFormRequestDefinitions = ''
    newApiRequestDefinitions = ''
    updateApiRequestDefinitions = ''
    argumentParser = ''
    argumentAggParser = ''
    instanceParams = ''
    publicHeaderRenderFields = ''
    publicRenderFields = ''
    renderFields = ''
    relationshipFieldsImports = ''
    relationshipJoins = ''
    relationshipReturns = ''
    contextData = ''
    renderUpdateFields = ''
    tableHeaders = ''
    tableValues = ''
    relationshipQueryAddColumns = ''
    xyzQueryAddColumns = ''

    count = 0

    for key, value in fields.items():
        friendly_name = (key.capitalize()).replace('_', ' ')
        instanceNames += "        self.{} = {}\n".format(key, key)
        instanceDictNames += "			'{}':self.{}\n".format(key, key)

        if value['relationship']:
            columns += "    {} = db.Column(db.{}, db.ForeignKey('{}.id'), nullable={}, default={}, unique={}, index={})\n".format(key,
                                                                                                                        value['dataType'],
                                                                                                                        value['relationship'],
                                                                                                                        value['nullable'],
                                                                                                                        value['default'],
                                                                                                                        value['unique'],
                                                                                                                        value['index'])

            relationshipFieldsImports += "from app.mod_{}.models import {}\n".format(value['relationship'],
                                                                                                value['relationship'].capitalize())

            relationshipJoins += "                .join({}.{})\n".format(model, value['relationship'])

            relationshipReturns += "    {} = {}.query.all()\n".format(value['relationship'],
                                                                                        value['relationship'].capitalize())

            contextDataArr.append("\n        '{}': {}".format(value['relationship'],value['relationship']))

            columns += "    {} = db.relationship('{}', remote_side='{}.id', lazy='joined', innerjoin=True)\n".format(value['relationship'],
                                                                                                # secrets.token_urlsafe(3),
                                                                                                value['relationship'].capitalize(),
                                                                                                value['relationship'].capitalize())

            columns += """
    # @aggregated('{}_count', db.Column(db.Integer))
    # def {}_count(self):
    #     return db.func.count('1')\n""".format(value['relationship'],
                                                value['relationship'])
        else:
            columns += "    {} = db.Column(db.{}, nullable={}, default={}, unique={}, index={})\n".format(key,
                                                                                        value['dataType'],
                                                                                        value['nullable'],
                                                                                        value['default'],
                                                                                        value['unique'],
                                                                                        value['index'])
        
        grapheneColumns += "    {} = graphene.{}\n".format(key,
                                            value['grapheneDataType']
                                            )
            
        
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
        
        if value['dataType'] == 'Date':
            updateApiRequestDefinitions += "        data.{} = fn.convert_to_python_data_type('date')(api.payload['{}'])\n".format(key, key)
        elif value['dataType'] == 'DateTime':
            updateApiRequestDefinitions += "        data.{} = fn.convert_to_python_data_type('datetime')(api.payload['{}'])\n".format(key, key)
        else:
            updateApiRequestDefinitions += "        data.{} = api.payload['{}']\n".format(key, key)
        
        renderFields += """
                                <div class="p-1 text-danger" style="{}% if not form.{}.errors %{} display:none; {}% endif %{}">
                                    {}% if form.{}.errors %{}
                                        {}% for error in form.{}.errors %{}
                                            {} error {}
                                        {}% endfor %{}
                                    {}% endif %{}
                                </div>
                                <div class="form-group row">
                                    <label for="{}" class="col-sm-2 control-label">{}</label>

                                    {}
                                </div>
        """.format("{", key, "}", "{", "}", "{", key, "}", "{", key, "}", "{{", "}}", "{", "}", "{", "}", key, friendly_name.replace('_'," "), getHtmlCreateInput(value['dataTypeLower'], key, friendly_name, value['relationship'], value['relationship_display_value']))

        if count == 0:
            publicHeaderRenderFields += """
                                                    <h3 class="card-title text-capitalize">{}value.{}{}</h3>
            """.format("{{", key, "}}")
            count = 1

        publicRenderFields += """
                                                    <p>
                                                        {}value.{}{}
                                                    </p>
        """.format("{{", key, "}}")
        renderUpdateFields += """
                                <div class="p-1 text-danger" style="{}% if not form.{}.errors %{} display:none; {}% endif %{}">
                                    {}% if form.{}.errors %{}
                                        {}% for error in form.{}.errors %{}
                                            {} error {}
                                        {}% endfor %{}
                                    {}% endif %{}
                                </div>
                                <div class="form-group row">
                                    <label for="{}" class="col-sm-2 control-label">{}</label>

                                    {}
                                </div>
        """.format("{", key, "}", "{", "}", "{", key, "}", "{", key, "}", "{{", "}}", "{", "}", "{", "}", key, friendly_name.replace('_'," "), getHtmlUpdateInput(value['dataTypeLower'],key, friendly_name, value['relationship'],value['relationship_display_value']))
        tableHeaders += """
                        <th>
                            {}
                        </th>
        """.format(friendly_name.replace('_'," "))

        if value['relationship']:
            tableValues += """
                                        <td>
                                            {} value.{}_{} {}
                                        </td>
            """.format("{{", value['relationship'], value['relationship_display_value'], "}}")
            
            relationshipQueryAddColumns += """                    {}.{}.label('{}_{}'),
            """.format(value['relationship'].capitalize(), value['relationship_display_value'],value['relationship'], value['relationship_display_value'])
        else:
            tableValues += """
                                        <td>
                                            {} value.{} {}
                                        </td>
            """.format("{{", key, "}}")
        
            xyzQueryAddColumns += """                    {}.{}.label('{}'),
            """.format(module.capitalize(), key, key)
        
        feildNames.append(key)

        if value['dataType'] == 'Date':
            newFormRequestDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('date')(request.form.get('{}'))".format(key, key))
        elif value['dataType'] == 'DateTime':
            newFormRequestDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('datetime')(request.form.get('{}'))".format(key, key))
        elif value['dataType'] == 'Boolean':
            newFormRequestDefinitionsArr.append("\n            {} = True if request.form.get('{}') == 'True' else False".format(key, key))
        else:
            newFormRequestDefinitionsArr.append("\n            {} = request.form.get('{}')".format(key, key))
        
        if value['dataType'] == 'Date':
            newBrokerDataDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('date')(data.get('{}', None))".format(key, key))
        elif value['dataType'] == 'DateTime':
            newBrokerDataDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('datetime')(data.get('{}', None))".format(key, key))
        elif value['dataType'] == 'Boolean':
            newBrokerDataDefinitionsArr.append("\n            {} = True if data.get('{}', None) == 'True' else False".format(key, key))
        else:
            newBrokerDataDefinitionsArr.append("\n            {} = data.get('{}', None)".format(key, key))
        
        if value['dataType'] == 'Date':
            updateFormRequestDefinitionsArr.append("\n        data.{} = fn.convert_to_python_data_type('date')(request.form.get('{}'))".format(key, key))
        elif value['dataType'] == 'DateTime':
            updateFormRequestDefinitionsArr.append("\n        data.{} = fn.convert_to_python_data_type('datetime')(request.form.get('{}'))".format(key, key))
        elif value['dataType'] == 'Boolean':
            updateFormRequestDefinitionsArr.append("\n        data.{} = True if request.form.get('{}') == 'True' else False".format(key, key))
        else:
            updateFormRequestDefinitionsArr.append("\n        data.{} = request.form.get('{}')".format(key, key))
        
        if value['dataType'] == 'Date':
            newApiRequestDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('date')(api.payload['{}'])".format(key, key))
        elif value['dataType'] == 'DateTime':
            newApiRequestDefinitionsArr.append("\n            {} = fn.convert_to_python_data_type('datetime')(api.payload['{}'])".format(key, key))
        else:
            newApiRequestDefinitionsArr.append("\n            {} = api.payload['{}']".format(key, key))
        

    contextData = str((','.join(item for item in contextDataArr)))
    instanceParams = str((', '.join(item for item in feildNames)))
    formDefinitions = str((''.join(item for item in formDefinitionsArr)))
    newBrokerDataDefinitions = str((','.join(item for item in newFormRequestDefinitionsArr)))
    newFormRequestDefinitions = str((','.join(item for item in newFormRequestDefinitionsArr)))
    updateFormRequestDefinitions = str((''.join(item for item in updateFormRequestDefinitionsArr)))
    newApiRequestDefinitions = str((','.join(item for item in newApiRequestDefinitionsArr)))
    argumentParser = str((','.join(item for item in argumentParserArr)))
    argumentAggParser = str((','.join(item for item in argumentAggParserArr)))

    newBrokerDataDefinitions = newBrokerDataDefinitions.lstrip('\n')
    newFormRequestDefinitions = newFormRequestDefinitions.lstrip('\n')
    updateFormRequestDefinitions = updateFormRequestDefinitions.lstrip('\n')
    newApiRequestDefinitions = newApiRequestDefinitions.lstrip('\n')
    updateApiRequestDefinitions = updateApiRequestDefinitions.rstrip('\n')
    argumentParser = argumentParser.lstrip('\n')
    argumentAggParser = argumentAggParser.lstrip('\n')
    columns = columns.rstrip('\n')
    relationshipFieldsImports = relationshipFieldsImports.rstrip('\n')
    relationshipJoins = relationshipJoins.rstrip('\n')
    relationshipReturns = relationshipReturns.rstrip('\n')
    grapheneColumns = grapheneColumns.rstrip('\n')
    newApiAggregateDefinitions = newApiAggregateDefinitions.rstrip(',\n')
    newApiAggregateObjectDefinitions = newApiAggregateObjectDefinitions.rstrip(',\n')
    instanceNames = instanceNames.rstrip('\n')
    instanceDictNames = instanceDictNames.rstrip('\n')
    friendly_name = friendly_name.rstrip('\n')
    formDefinitions = formDefinitions.lstrip('\n')
    renderFields = renderFields.rstrip('\n')
    publicHeaderRenderFields = publicHeaderRenderFields.rstrip('\n')
    publicRenderFields = publicRenderFields.rstrip('\n')
    renderUpdateFields = renderUpdateFields.rstrip('\n')
    tableHeaders = tableHeaders.rstrip('\n')
    tableValues = tableValues.rstrip('\n')
    relationshipQueryAddColumns = relationshipQueryAddColumns.rstrip('\n')
    xyzQueryAddColumns = xyzQueryAddColumns.rstrip('\n')

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
            destination.write("try:\n")
            destination.write("    from app.mod_" + module + ".controllers import mod_public_" + module + " as " + module + "_public_module  # noqa: E402\n")
            destination.write("    from app.mod_" + module + ".controllers import mod_admin_" + module + " as " + module + "_admin_module  # noqa: E402\n")
            destination.write("except ImportError as e:\n")
            destination.write("    print(ImportError.__class__.__name__ + ': ' + str(e))\n")
            destination.write("except Exception as e:\n")
            destination.write("    print(Exception.__class__.__name__ + ': ' + str(e))\n")
        if "# register_blueprint new xyz_module" in line:
            destination.write("# " + module + "\n")
            destination.write("try:\n")
            destination.write("    app.register_blueprint(" + module + "_public_module)\n")
            destination.write("    app.register_blueprint(" + module + "_admin_module)\n")
            destination.write("except Exception as e:\n")
            destination.write("    print(Exception.__class__.__name__ + ': ' + str(e))\n")
        if "# new xyz api resources" in line:
            destination.write("# " + module + "\n")
            destination.write("try:\n")
            destination.write("    from app.mod_" + module + ".api_controllers import ns as " + module.capitalize() + "_API  # noqa: E402\n")
            destination.write("except Exception as e:\n")
            destination.write("    print(Exception.__class__.__name__ + ': ' + str(e))\n")

    source.close()
    destination.close()

    #################
    # remove source #
    #################

    os.remove('app/__init__.py~')

    ##############################################################
    # Copy App GraphQL query.py for manage source -> destination #
    ##############################################################

    shutil.copy2('app/mod_graphql/query.py', 'app/mod_graphql/query.py~')

    ################################
    # manage source -> destination #
    ################################

    source = open('app/mod_graphql/query.py~', "r")
    destination = open('app/mod_graphql/query.py', "w")

    for line in source:
        destination.write(line)
        if "# import new xyz_model and xyz_type" in line:
            destination.write("# " + module + "\n")
            destination.write("from app.mod_" + module + ".models import " + module.capitalize() + " as " + module.capitalize() + "Model  # noqa: E402\n")
            destination.write("from app.mod_" + module + ".types import " + module.capitalize() + " as " + module.capitalize() + "Types  # noqa: E402\n")
        if "# new xyz_model connection" in line:
            destination.write("    # " + module + "\n")
            destination.write("    all_" + module + " = SQLAlchemyConnectionField(" + module.capitalize() + "Types.connection)\n")

    source.close()
    destination.close()

    #################
    # remove source #
    #################

    os.remove('app/mod_graphql/query.py~')


    ##############################################################
    # Copy App GraphQL mutation.py for manage source -> destination #
    ##############################################################

    shutil.copy2('app/mod_graphql/mutation.py', 'app/mod_graphql/mutation.py~')

    ################################
    # manage source -> destination #
    ################################

    source = open('app/mod_graphql/mutation.py~', "r")
    destination = open('app/mod_graphql/mutation.py', "w")

    for line in source:
        destination.write(line)
        if "# import new xyz_model and xyz_type, input" in line:
            destination.write("# " + module + "\n")
            destination.write("from app.mod_" + module + ".models import " + module.capitalize() + " as " + module.capitalize() + "Model  # noqa: E402\n")
            destination.write("from app.mod_" + module + ".types import " + module.capitalize() + " as " + module.capitalize() + "Types, Create" + module.capitalize() + "Input  # noqa: E402\n")
        if "# new create xyz class" in line:
            destination.write("\n# " + module)
            destination.write("""
class Create_{}(graphene.Mutation):
    {} = graphene.Field(lambda: {}Types)
    ok = graphene.Boolean()

    class Arguments:
        input = Create{}Input(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = graphql_input_into_dictionary(input)
        {} = {}Model(**data)
        db.session.add({})
        db.session.commit()
        ok = True
        return Create_{}({}={}, ok=ok)

            """.format(
                module.capitalize(),
                module,
                module.capitalize(),
                module.capitalize(),
                module,
                module.capitalize(),
                module,
                module.capitalize(),
                module,
                module
            ))
    
        if "# register new createXyz" in line:
            destination.write("    # " + module + "\n")
            destination.write("    create" + module.capitalize() + " = Create_" + module.capitalize() + ".Field()\n")

    source.close()
    destination.close()

    #################
    # remove source #
    #################

    os.remove('app/mod_graphql/mutation.py~')


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
                if('sql_alch_broker.py' in s):
                    replaceTextBetweenTags(s, '# start new broker data feilds', '# end new broker data feilds', '            ', '')
                if('controllers.py' in s):
                    replaceTextBetweenTags(s, '# start new request feilds', '# end new request feilds', '        ', '')
                    replaceTextBetweenTags(s, '# start update request feilds', '# end update request feilds', '    ','')
                if('forms.py' in s):
                    replaceTextBetweenTags(s, '# start new form definitions', '# end new form definitions', '    ', '')
                if('types.py' in s):
                    replaceTextBetweenTags(s, '# start new graphene attribute fields', '# end new field definitions', '    ', '')
                if('models.py' in s):
                    replaceTextBetweenTags(s, '# start new field definitions', '# end new graphene attribute fields', '    ', '')
                    replaceTextBetweenTags(s, '# start new instance fields', '# end new instance fields', '        ', '')
                    replaceTextBetweenTags(s, '# start new instance dict fields', '# end new instance dict fields', '            ', '')
                if('index.html' in s):
                    replaceTextBetweenTags(s, '<!-- start new table headers -->', '<!-- end new table headers -->', '                    ', '')
                    replaceTextBetweenTags(s, '<!-- start new table values -->', '<!-- end new table values -->', '                        ', '')
                    replaceTextBetweenTags(s, '<!-- start new publicHeaderRenderFields -->', '<!-- end new publicHeaderRenderFields -->', '                                                    ', '')
                    replaceTextBetweenTags(s, '<!-- start new publicRenderFields -->', '<!-- end new publicRenderFields -->', '                                                    ', '')
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
                    if "# start new broker data feilds" in line:
                        destination.write(newBrokerDataDefinitions)
                    if "# start new request feilds" in line:
                        destination.write(newFormRequestDefinitions)
                    if "# Import module models (e.g. User)" in line:
                        destination.write(relationshipFieldsImports)
                    if "# relationship join" in line:
                        destination.write(relationshipJoins)
                    if "# Relationship returns" in line:
                        destination.write(relationshipReturns)
                    if "# Relationship context_data" in line:
                        destination.write(contextData)
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
                    if "# start new graphene attribute fields" in line:
                        destination.write(grapheneColumns)
                    if "# start new instance fields" in line:
                        destination.write(instanceNames)
                    if "# start new instance dict fields" in line:
                        destination.write(instanceDictNames)
                    if "<!-- start new render fields -->" in line:
                        destination.write(renderFields)
                    if "<!-- start new render_update fields -->" in line:
                        destination.write(renderUpdateFields)
                    if "<!-- start new publicHeaderRenderFields -->" in line:
                        destination.write(publicHeaderRenderFields)
                    if "<!-- start new publicRenderFields -->" in line:
                        destination.write(publicRenderFields)
                    if "<!-- start new table headers -->" in line:
                        destination.write(tableHeaders)
                    if "<!-- start new table values -->" in line:
                        destination.write(tableValues)
                    if "# relationship query add columns" in line:
                        destination.write(relationshipQueryAddColumns)
                    if "# Xyz query add columns" in line:
                        destination.write(xyzQueryAddColumns)
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