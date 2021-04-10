import click
from ... import create_module

@click.command()
@click.option('--module', default=1, 
                    help='Name of module to create. It must have a JSON file to create from')
def cli(module):
    """Generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module is the name of the module you input"""

    file = 'app/generated_config/models/'+ module + "/models.json"
    
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        create_module(data[module])

if __name__ == '__main__':
    cli()