# Business Driven App (BDA)
## A Rapid Application Development (RAD) tool to assist with building flask python applications. Helping you build applications fast, right, and for the Future.

> **Note:** Still under Development

> Flask BDA is a low-code platform which provides the tools for companies to raplidly develop and deploy secure applications that run on any device.
> 
> We change the way software is built so you can rapidly create and deploy critical applications of any size that evolve with your business.
> 
> Developers can build and deploy a full range of applications - from consumer apps to critical internal business systems - designed to help developers deliver secure applications quickly and efficiently so apps are delivered in weeks and even days.
>
> Flask BDA provides Full-stack development from; UI, business processes, custom logic, and data models to create cross-platform apps out of the box. providing you a scaffold that you can add your own code when needed. with no lock-in ever.

## Overview
* [Requirements](#requirements)
* [Quickstart](#quickstart)
* [Project Structure](#project-structure)
* [Create new CRUD module](#create-new-crud-module)
* [Environments](#environments)
* [Testing](#testing)
* [Features List](#features-list)
* [Project Structure](#project-structure)
* [Glossary](#glossary)

# Requirements
* Download and install Python (https://www.python.org/downloads/) if you do not already have it installed.
    * Ensure pip is installed (pip should be installed already because it comes with the latest versions of python) in case it is not, please install it from here: https://pip.pypa.io/en/stable/installing/

# Quickstart
* Ensure you have installed the [requirements](#requirements)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
```
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
```
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py

```
---

* Fill in your project name when prompted eg:
    * Please ensure you put quotes around your project name to prevent errors eg: `"My Awesome Project"`
```
Project Name:
"My Awesome Project"
```
> **Note:** You will notice this creates a folder in the same path as the file: "create_project_git.py".
> This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`

# Create new [CRUD](#crud) module

> A module is a self-contained component, making it easier to manage as the program grows. Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views
> 
> When you create a new CRUD module, all the elements from the folder `create_module_template` are copied into the app directory and renamed to the module name you provide by replacing all `xyz` values with your module name and adding additional data model information as described below

### create_module_template structure for `Projects` module added to app
```
├── project_name
       └── app
            ├── mod_projects
            │     ├── api_controllers.py
            │     ├── controllers.py
            │     ├── forms.py
            │     └── models.py
            └── templates
                  └── projects
                       ├── admin
                       │    ├── create.html
                       │    ├── edit.html
                       │    ├── index.html
                       │    └── show.html
                       └── public
                            └── public_list.html
```

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
         ,'LargeBinary'): `String`
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
* [Local python venv](#local-environment)
* [Docker](#docker-environment)
* [AWS Serverless](#aws-serverless) (Still under Development)

## Local Environment

> To create and develop a local application we are using [virtualenv](https://pypi.org/project/virtualenv/) A tool for creating isolated virtual python environments.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

pip install virtualenv
virtualenv venv

venv\Scripts\activate

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
virtualenv venv

venv/bin/activate

pip install --no-cache-dir -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development

flask run

```

## Docker Environment

> To create and deploy a containerized application we are using [Docker](https://www.docker.com/) which helps developers and development teams build and ship apps. Docker is used for the building and sharing of containerized applications and microservices.

> NOTE if you are using [Github](https://github.com/) and have docker installed (details on how to install lower down), you will get a new image built every time you `push` or do a `pull_request` on Github, which is set up in the file: `docker-image.yml` however if you want to do this manually, please follow the following steps:4

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

## AWS Serverless

> **Note:** Still under development

> To create and deploy a serverless application we are using [The Serverless Framework](https://www.serverless.com/) whice allows for a zero-friction serverless development, allowing you to easily build apps that auto-scale on low cost, next-gen cloud infrastructure.
> 
> The Serverless framework is an open source tool that provides an easy YAML + CLI development and deployment to AWS, Azure, Google Cloud, Knative & more.

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

> **Note:** if the package does not install you may need to run the comand as an admin.
> 
> press the  "Windows-Key" type "cmd", "Right-Click" on the word "Command Prompt" and Select the option "Run as administrator" and then follow the previous steps again

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

> If you include additional python packages in your project don't forget to run a `pip freeze` from your terminal to ensure you get that correct packages for your deployments
>
> `pip freeze > requirements.txt`

# Testing

> 

There are 3 aspects of testing provided:
* CI/CD through [Github actions workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions) which is already set up to implement:
    * Python [flake8](https://flake8.pycqa.org/en/latest/) code [linting](#linting).
        * It displays the warnings in a per-file, merged output. Flake8 is a wrapper around these tools:
            * PyFlakes
            * pycodestyle
            * Ned Batchelder’s McCabe script
    * Python [unittest](https://docs.python.org/3/library/unittest.html) originally inspired by JUnit and has a similar flavor as major [unit testing](#unit-testing) frameworks in other languages.

# Python flake8

> **Note** To manually run Python unittest ensure that you have installed the [local environements](#local-environment)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

venv\Scripts\activate

flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=11 --max-line-length=127 --statistics

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
cd <Path To>/my_awesome_project

venv/bin/activate

flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

```

# Python unittest

> **Note** To manually run Python unittest ensure that you have installed the [local environements](#local-environment)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```
cd <Path To>/my_awesome_project

venv/bin/activate

python -m unittest discover

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```
cd <Path To>/my_awesome_project

venv/bin/activate

python -m unittest discover

```


# Features List
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
    * Configuration file "config.py" for quick access and management of environment and environment variables and default SEO
    * A Landing page with call to action and features
    * A 403 page which all forbidden pages goes to
    * A 404 page which all unknown pages goes to
    * .gitignore files with defaults
    * [Testing](#testing) with Python [flake8](https://flake8.pycqa.org/en/latest/) Linting and Test cases Python [unittest](https://docs.python.org/3/library/unittest.html)
    * CI/CD through [Github actions workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions)
    * Can run in any cloud or in your data center.
        * Server entry point file for shared hosting from "run.py" 
        * [Local virtual Python environment](#local-environment)
        * [Docker virual environment config](#docker-environment)
            * Removes tons of headaches when setting up your dev environment
            * Prevents issues such as "well, it worked on my machine!"
        * [AWS Serverless yml config](#aws-serverless)
    * Great UI by default with [Tailwind](https://tailwindcss.com/)
        * Highly customizable and flexable
        * Pre-setup via CDN
        * Versatile
        * There is no JavaScript. And because of that, you can easily bind it with any JavaScript framework of your choice


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
    * SQLAlchemy Events. Pre-configured `before` and `after` changes on a data model `event listeners` for:
        * `Insert`
        * `Update`
        * `Delete` 
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

## Project Structure
```
├── project_name
       ├── app
       │    ├── mod_auth
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     ├── forms.py
       │    │     └── models.py
       │    ├── static
       │    │     ├── css
       │    │     ├── images
       │    │     ├── js
       │    │     ├── manifest.json
       │    │     └── sw.js
       │    ├── templates
       │    │     ├── admin
       │    │     ├── auth
       │    │     ├── public
       │    │     ├── 403.html
       │    │     ├── 404.html
       │    │     └── index.html
       │    └── __init__.py
       ├── create_module_template
       │    ├── mod_xyz
       │    │     ├── api_controllers.py
       │    │     ├── controllers.py
       │    │     ├── forms.py
       │    │     └── models.py
       │    └── templates
       │          └── xyz
       │               ├── admin
       │               │    ├── create.html
       │               │    ├── edit.html
       │               │    ├── index.html
       │               │    └── show.html
       │               ├── public
       │                    └── public_list.html
       ├── .dockerignore
       ├── .gitignore
       ├── app.db
       ├── config.py
       ├── create_module.py
       ├── Dockerfile
       ├── LICENSE
       ├── README.md
       ├── requirements.txt
       ├── run.py
       └── serverless.yml
```

# Glossary
## Modules
### Introduction
> A module is a part of a program. Programs are composed of one or more independently developed modules that when combined create the  program. 
> 
> A module is a self-contained component, making it easier to manage as the program grows.
> 
> Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views

## Controllers:
### Introduction
> Controllers can group related request handling logic into a single class. For example, a UserController class might handle all incoming requests related to users, including showing, creating, updating, and deleting users.

## CRUD
### Definition
> Create, Read, Update, and Delete ("CRUD")

## Linting
### Definition
> Linting is the automated checking of your source code for programmatic and stylistic errors. This is done by using a lint tool (otherwise known as linter). A lint tool is a basic static code analyzer.
> 
> lint, or a linter, is a static code analysis tool used to flag programming errors, bugs, stylistic errors, and suspicious constructs.

## Unit Testing
### Definition
> In computer programming, unit testing is a software testing method by which individual units of source code—sets of one or more computer program modules together with associated control data, usage procedures, and operating procedures—are tested to determine whether they are fit for use.
