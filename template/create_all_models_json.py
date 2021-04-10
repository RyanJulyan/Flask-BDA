
import os
import json

def get_files(src):
    models = {}
    for item in os.listdir(src):
        s = os.path.join(src, item)
        file = s + "/models.json"
        with open(file, 'r') as json_file:  # Use file to refer to the file object
            data = json.load(json_file)
            models.update(data)
    return models


def create_models_json():
    models = get_files('app/generated_config/models')

    with open('app/static/db_models/all_models.json', 'w') as outfile:
        json.dump(models, outfile, indent=4, sort_keys=True)

    with open('app/static/db_models/all_models.js', 'w') as outfile:
        variable_models = 'let all_models = ' + json.dumps(models)
        # variable_models = variable_models.replace('\"','')
        # variable_models = variable_models.replace('"','')
        outfile.write(variable_models)

if __name__ == "__main__":
    create_models_json()

