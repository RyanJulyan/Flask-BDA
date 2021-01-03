# Business Driven App (BDA)
## a Rapid Application Development (RAD) tool to assist with building flask python applications.

## Overview
* [Requirements](#requirements)
* [Quickstart](#quickstart)
* [Project Features](#features)
* [Create new CRUD module](#create-new-crud-module)
* [Environments](#environments)

# Requirements
* Download and install Python (https://www.python.org/downloads/)
    * Ensure pip is installed should be because it comes with the latest versions of python but in case it is not, please install it from herre: https://pip.pypa.io/en/stable/installing/

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
pip install virtualenv

```
> **Note:** if the package does not install you may need to run the comand as an admin.
> 
> press the  "Windows-Key" type "cmd", "Right-Click" on the word "Command Prompt" and Select the option "Run as administrator"

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
pip install virtualenv

```

# Quickstart
* Ensure you have installed the [requirements](#requirements)
### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal

---

* Copy, paste and run the following code in the terminal
    * This will download the required create_project python file and run it to help you start a project
```
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py

```

* Fill in your project name when prompted eg:
```
Project Name:
My Awesome Project
```
> **Note:** You will notice this creates a folder in the same path as the file: "create_project_git.py".
> This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`

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
    * Local virtual Python environment
    * Docker virual environment config
    * AWS Serverless yml config
    * Tailwind for Layouts / design
        * Highly customizable and flexable
        * Pre-setup via CDN
        * Versatile
        * There is no JavaScript. And because of that, you can easily bind it with any JavaScript framework of your choice

---

* Create custom [module](#Modules) files and folders that fit into the flask project structure from `create_module.py` file with prompts to create the following:
    * Model
        * Dynamically create table data model 
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
            * Public
                * View ../xyz/ [list elements] `public_list`
            * Admin
                * View ../admin/xyz/ [list elements] `index`
                * View ../admin/xyz/create [single element] `create`
                * POST URL ../admin/xyz/store [single element] `store`
                * View ../admin/xyz/show/{id} [single element] `show`
                * View ../admin/xyz/edit/{id} [single element] `edit`
                * PUT URL ../admin/xyz/update/{id} [single element]`update`
                * DELETE URL ../admin/xyz/destroy/{id} [single element] `destroy`
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

```
├── dream-team
       ├── app
       │   ├── __init__.py
       │   ├── templates
       │   ├── static
       │   ├── models.py
       │   └── views.py
       ├── config.py
       ├── requirements.txt
       └── run.py
```

# Create new [CRUD](#CRUD) module

> A module is a self-contained component, making it easier to manage as the program grows. Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views

* To create your own custom modules, Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * Fill in the instructions eg:
```
Module Name:
`Projects`
```
* You can then create a table with columns by following the prompts eg:
```
Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): `name`
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
        'LargeBinary': `String`
String Length (1-256): `256`
Is name nullable ('True', 'False'): `false`
Is name unique ('True', 'False'): `true`
Default value: 

```

> **Note:** this will keep looping until you type and submit the words: "STOP_CREATING_FIELDS". 
> 
> This allows you to create multiple fields for your module quickly and easily

# Environments
There are 3 out of the box environments supported with instructions on how to configure each for  `Windows / Linux / Mac` and you could run them at the same time if you want.
* [Local python env](#local-environment)
* [Docker](#docker-environment)
* [AWS Serverless](#aws-serverles) (Still under Development)

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
* Open browser and install docker desktop
    * Go to: https://hub.docker.com/editions/community/docker-ce-desktop-windows/ to get the installer
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

## AWS Serverles
### Via npm
```
npm update -g serverless

```
### Windows
* Open browser and install Chocolatey from the 
    * Go to: https://chocolatey.org/install to get the installer
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
choco install serverless

serverless

```
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

serverless deploy

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
curl -o- -L https://slss.io/install | bash

serverless

```
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
cd <Path To>/my_awesome_project

serverless deploy

```

> if you include additional python packages in your project don't forget to run a pip freeze to ensure you get that correct packages for your deployments
>
> `pip freeze > requirements.txt`

# Glossary
## Modules
> A module is a part of a program. Programs are composed of one or more independently developed modules that when combined create the  program. 
> 
> A module is a self-contained component, making it easier to manage as the program grows.
> 
> Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views

## Controllers:
### introduction
> Controllers can group related request handling logic into a single class. For example, a UserController class might handle all incoming requests related to users, including showing, creating, updating, and deleting users.

## CRUD
## Definition
> Create, Read, Update, and Delete ("CRUD")