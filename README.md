# Business Driven App (BDA)
## a Rapid Application Development (RAD) tool to assist with building flask python applications.

## Overview
* [Project Features](#features)
* [Requirements](#requirements)
* [Quickstart](#quickstart)
* [Create new CRUD module](#create-new-crud-module)
* [Environments](#environments)

### Features
* Single file run and setup
* Starter flask project which builds a project folder structures with
    * Flask microframework
        * Quick and easy
        * Ability to scale up
        * One of the most popular Python web application frameworks.
        * Doesn't enforce any dependencies or project layout.
    * Progressive Web App (PWA) to make it more friendly towards desktop and allow native installs from the web, chache for offline support, page sharing and push notifications etc
    * SEO ready page index template file
    * Isolated module code and templates
    * Configuration file "config.py" for quick access and management of environment and environment variables
    * Server entry point file for shared hosting from "run.py" 
    * A Landing page with call to action and features
    * A 403 page which all forbidden pages goes to
    * A 404 page which all unknown pages goes to
    * .gitignore files with defaults
    * Docker virual environment
    * Local virtual environment
    * Tailwind for Layouts / design
        * Highly customizable and flexable
        * Pre-setup via CDN
        * Versatile
        * There is no JavaScript. And because of that, you can easily bind it with any JavaScript framework of your choice
* Create custom module files and folders that fit into the flask project structure from "create_module.py" file with prompts to create the following:
    * Model
    * Web Controller
        * Public
            * `public_list`
        * Admin
            * `index`
            * `create`
            * `store`
            * `show`
            * `edit`
            * `update`
            * `destroy`
    * API Controller
        * ListResource
            * `get`
            * `post`
        * Resource
            * `get`
            * `update`
            * `delete`
    * Forms
    * URL's (prefixed by the module name)
        * Web Routes:
            * View ../xyz/ [list elements] `index`
            * View ../xyz/create [single element] `create`
            * POST URL ../xyz/store [single element] `store`
            * View ../xyz/show/{id} [single element] `show`
            * View ../xyz/edit/{id} [single element] `edit`
            * PUT URL ../xyz/update/{id} [single element]`update`
            * DELETE URL ../xyz/destroy/{id} [single element] `destroy`
        * API Routes:
            * GET URL ../api/xyz [list elements] `get`
            * POST URL ../api/xyz [single element] `post`
            * GET URL ../api/xyz/{id} [single element] `get`
            * PUT URL ../api/xyz/{id} [single element] `update`
            * DELETE URL ../api/xyz/{id} [single element]`delete`
    * Views for:
        * Public
            * `public_list.html` (list elements)
        * Admin
            * `index.html` (list elements)
            * `create.html` (single element form)
            * `show.html` (single element)
            * `edit.html` (single element form)

# Requirements
* Python (https://www.python.org/downloads/) with PIP (https://pip.pypa.io/en/stable/installing/)
    * `pip install virtualenv`
    * `pip install PyGithub`

# Quickstart
* Open and run the file: `<Path To>/create_project_git.py` from the root of BDA (you can download just that file if you wish)
    * Fill in the instructions eg:
```
Project Name:
My Awesome Project
```
* You will notice this creates a folder in the same path as the file: "create_project_git.py".
    * This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`

# Create new CRUD module
* Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * Fill in the instructions eg:
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
There are 2 out of the box environments supported with instructions on how to configure each for  `Windows / Linux / Mac` and you could run them at the same time if you want.
* [Local python env](#local-environment)
* [Docker](#docker-environment)

## Local Environment
### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

pip install virtualenv
virtualenv env

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

pip install virtualenv
virtualenv env

env/bin/activate

pip install --no-cache-dir -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development

flask run

```

## Docker Environment
### Windows
* Open browser and install docker desktop from the 
    * Go to: https://hub.docker.com/editions/community/docker-ce-desktop-windows/
* "Windows-Key + R" will show you the 'RUN' box
    * Type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
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
docker run -it -p 5000:5000 flask_app

```