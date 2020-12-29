# Business Driven App (BDA)
## is a Rapid Application Development (RAD) tool meant to assist with structure and building applications.

### This project currently offers the following features:
* Single file run and setup
* Starter flask project which builds a project folder structures with  
    * Progressive Web App (PWA) to make it more friendly towards desktop and allow native installs from the web, chache for offline support, page sharing and push notifications etc
    * SEO ready page index template file
    * Isolated module code and templates
    * Configuration file "config.py" for quick access and management of environment and environment variables
    * Server entry point file for shared hosting from "run.py" 
    * A 403 page which all forbidden pages goes to
    * A 404 page which all unknown pages goes to
    * .gitignore files with defaults
    * Docker virual environment
    * Local virtual environment
* Create custom module files and folders that fit into the flask project structure from "create_module.py" file with prompts
    * Creates:
        * Model
        * Controlle
        * Forms
        * URL's (prefixed by the module name)
            * Routes:
                * index
                * 
        * Views (Templates for index)


# Requirements
* Python (https://www.python.org/downloads/) with PIP (https://pip.pypa.io/en/stable/installing/)
    * pip install virtualenv
    * pip install PyGithub

# Quickstart
* Open and run the file: `<Path To>/create_project_git.py` from the root of BDA (you can download just that file if you wish)
    * fill in the instructions eg:
```
Project Name:
My Awesome Project
```
* you will notice this creates a folder in the same path as the file: "create_project_git.py".
    * this folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores

# Create new CRUD module
* Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * fill in the instructions eg:
```
Module Name:
Projects
```
* You can then create a table with columns by following the prompts eg:
```
Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): name
What datatype is name
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
        'LargeBinary': String
String Length (1-256): 256
Is name nullable ('True', 'False'): false
Is name unique ('True', 'False'): true
Default value: 

``` 

# Environments
There are 2 out of the box environments supported with instructions on how to configure each for  `Windows / Linux / Mac`
* Local python env
* Docker

## Local Environment
### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

env\Scripts\activate

pip install --no-cache-dir -r requirements.txt

set FLASK_APP=app
set FLASK_ENV=development

flask run

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
cd <Path To>/my_awesome_project

env/bin/activate

pip install --no-cache-dir -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development

flask run

```

## Docker Environment
### Windows
* Open browser and install docker desktop from the 
    * go to: https://hub.docker.com/editions/community/docker-ce-desktop-windows/
* "Windows-Key + R" will show you the 'RUN' box
    * type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

docker build -t flask_app:latest .
docker run -p 5000:5000 flask_app

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

systemctl start docker

```
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
cd <Path To>/my_awesome_project

docker build -t flask_app:latest .
docker run -p 5000:5000 flask_app

```