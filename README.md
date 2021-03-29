# Flask Business Driven App (BDA)
## A Cross-platform, Multi-tenant, SAAS ready, Rapid Application Development (RAD) tool to assist with building flask python applications. Helping you build applications fast, right, and for the Future.

> **Note:** Still under Development

# Why use Flask-BDA

> Other solutions such as [Tableau](https://www.tableau.com/), [Power BI](https://powerbi.microsoft.com/en-us/) and [Amazon QuickSight](https://aws.amazon.com/quicksight/), while fantastic tools, focus on reporting but do not let you edit or add data to the platforms when needed, meaning you require additional solutions or software to acheive your business goals

> Solutions like [Excel](https://www.microsoft.com/en-za/microsoft-365/excel) are accessable to everyone and give you all the flexibility you might need, but your data is scattered and does not easily allow for a shared source of truth for your team and clients, it is very easy for excel documents to be out of sync or even shared, opening your company up to a security risk.

> Flask-BDA helps you by providing you the control to deliver raplid, secure, Full-stack applications 3-5x (3-5 times) faster. With no vendor or environment lock-in, ever.

> Automatically deal with the tedious aspects that slow down software development
> * Create & manage all database connections and complex queries.
> * Application security with user and role-based access control
> * Automatic audits on every action

> Flask-BDA is a [low-code platform](#low-code-platform) (meaning we will help you by writing a lot of the code for you) which provides the tools for companies to raplidly develop and deploy secure applications that run on any device.
> 
> We change the way software is built so you can rapidly create and deploy critical applications of any size that evolve with your business saving you time & money.
> 
> Developers can build and deploy a full range of applications - from consumer apps to critical internal business systems - designed to help developers deliver secure applications quickly and efficiently so apps are delivered in weeks and even days.
>
> Flask-BDA provides Full-stack development from; UI, business processes, custom logic, and data models to create cross-platform apps out of the box. providing you a scaffold that you can add your own code when needed. with no lock-in ever.
> 
> With pre-configured development environments, we reduce the pain (and cost) of getting to market, giving you the flexibility to choose where and how to deploy.

> Free and Developer-Friendly,
> Flask-BDA is a free to use, source available, application development tool with a developer-friendly [license](#license).

# Costs

> Flask-BDA is completely **FREE** to use for comercial and personal projects.

> However, Software development is always a costly exercise:
> * You will need to pay one or multiple Software Developers, Business Analysts, Designers, Project Managers and other team members to  build your product.
> * Your product is never finished. A software project will always need continued development.
>     * When you deliver a product, your competition is already working on new and improved features and you need to be able to stay ahead, or at least keep up or users will move to your competition.
>     * Once you start using your product, you and your team will think of new features that will make it even better and improve your processes.
>     * Continued maintenance. As users make use of the product, they will find ways to break it that you haven't thought of, and they need to be fixed.

## Rough Costing Table (2020) For Normal Development
| Project size                                                    | Initial cost |  Ongoing cost                         |
|-----------------------------------------------------------------|-------------:|--------------------------------------:|
| Small-sized projects (2 - 6 weeks of development)               |      $11 250 |     $563 - $1 125 (±10%) / per month  |
| Medium-sized projects (2 - 4 months of development)             |      $33 750 |  $1 563  - $3 375 (±10%) / per month  |
| Large-sized projects (6 - 18 months, or longer, of development) |     $156 250 |  $3 375 - $15 625 (±10%) / per month  |

## Rough Costing Table (2020) For Flask-BDA Development
| Project size                                                    | Initial cost |  Ongoing cost                        |
|-----------------------------------------------------------------|-------------:|-------------------------------------:|
| Small-sized projects (1 - 3 weeks of development)               |       $3 750 |      $188 - $375 (±10%) / per month  |
| Medium-sized projects (1 - 3 months of development)             |      $11 250 |    $375 - $1 125 (±10%) / per month  |
| Large-sized projects (2 - 6 months, or longer, of development)  |      $52 084 |  $1 125 - $5 208 (±10%) / per month  |

> With Flask-BDA you **DON'T LOOSE ANY of the flexibility of "Normal Development"** as it uses standarized development patterns and tried and tested technologies.

> Flask-BDA uses many Open Source technologies and leverages existing technology stacks, so that you can easily find other developers who use the same technologies, and you do not have to pay for costly licence fees or environment costs regardless of how much revenue your company makes, or where you are in your business.

# Overview
* [Why use Flask-BDA](#why-use-flask-bda)
* [Costs](#costs)
* [Process](#process)
* [Requirements](#requirements)
* [Quickstart](#quickstart)
* [Create new CRUD module](#create-new-crud-module)
* [Environments](#environments)
* [Installing Additional Python Packages](#installing-additional-python-packages)
* [OpenAPI/Swagger API](#openapiswagger-api)
* [Import API to Postman](#import-api-to-postman)
* [External API Requests](#external-api-requests)
* [Ajax Requests](#ajax-requests)
* [Testing](#testing)
* [Features List](#features-list)
* [Project Structure](#project-structure)
* [Glossary](#glossary)
* [License](#license)

# Process

## Step 1:
### Download pre-configured development environment

> Start your development with a quick and easy download a pre-configured development environment up and running in minutes.

> No complex setup required, only python is required.

## Step 2:
### Rapidly develop custom modules

> Create your own modules and data structures.

> Your data structures are saved as a data model allowing you to use different databases.

## Step 3:
### Fully functional pages

> Auto generated views fully functional interactive pages, easily managed per module.

> Out of the box, Admin and Mobile views are generated.

> API's are created automatically with a Swagger front-end and machine-friendly interface.

## Step 4:
### Customize

> Configure reports to your specific needs and share them with your team and clients.

> White your own custom code in an isolated module so you do not affect other modules.

## Step 5:
### Deploy

> Web & Mobile

> Environments include: Docker / AWS / Shared hosting.

# Requirements
* Download and install Python (https://www.python.org/downloads/) if you do not already have it installed.
    * Ensure pip is installed (pip should be installed already because it comes with the latest versions of python) in case it is not, please install it from here: https://pip.pypa.io/en/stable/installing/
        * To check if pip is installed you can run the following command in your terminal
```shell
python -m pip --version
```

# Quickstart

> To get started building your first project, with Flask-BDA follow the simple steps below to create your own pre-configured development environment up and running in minutes.

> In this quickstart we are going to create a project called `"My Awesome Project"`, however, you can call the project anything you want.

* Ensure you have installed the [requirements](#requirements)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py

```
---

* Fill in your project name when prompted eg:
    * Please ensure you put quotes around your project name to prevent errors eg: `"My Awesome Project"`
```python
Project Name:
"My Awesome Project"
```
> **Note:** You will notice this creates a folder in the same path as the file: "create_project_git.py".
> This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`

# Create new [CRUD](#crud) module

> A module is a self-contained component, making it easier to manage as the program grows. Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views
> 
> When you create a new CRUD module, all the elements from the folder `create_module_template` are copied into the app directory and renamed to the module name you provide by replacing all `xyz` values with your module name and adding additional data model information as described below

## How to create a new module

* To create your own custom modules, Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * Fill in the instructions eg:
```python
Module Name:
"Projects"
```
* You can then create a table with columns by following the prompts eg:
```python
Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): "name"
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
         ,'LargeBinary'): "String"
String Length (1-256): 256
Is name nullable ('True', 'False'): False
Is name unique ('True', 'False'): True
Default value: 

```

> **Note:** this will keep looping until you type and submit the words: "STOP_CREATING_FIELDS". 
> 
> This allows you to create multiple fields for your module quickly and easily

### App changes

> files and folders from the `create_module_template` folder are created for the `Projects` module, and then added to the `app` folder
>
> This will create a scaffolded admin pannel views, an API and public facing views and logic to allow you to imediately interact with the module you created.
> 
> From the admin pannel you will be able to perform the following actions: Create, Read, Update, and Delete ("CRUD") for your new modle.
> 
> The public facing views allows guest users (users not logged in) to see a view of the information provided

```
└── `my_awesome_project`
       └── app
            ├── generated_config
            │     └── models
            │          └── `projects`
            │               └── models.json
            └── `mod_projects`
                  ├── templates
                  │     ├── mobile
                  │     │    └── `projects`
                  │     │         ├── admin
                  │     │         │    ├── create.html
                  │     │         │    ├── edit.html
                  │     │         │    ├── index.html
                  │     │         │    └── show.html
                  │     │         └── public
                  │     │              └── public_list.html
                  │     └── `projects`
                  │          ├── admin
                  │          │    ├── create.html
                  │          │    ├── edit.html
                  │          │    ├── index.html
                  │          │    └── show.html
                  │          └── public
                  │               └── public_list.html
                  ├── api_controllers.py
                  ├── controllers.py
                  ├── forms.py
                  └── models.py
```

# Environments
There are 4 out of the box environments supported with instructions on how to configure each for  `Windows / Linux / Mac` and you could run them at the same time if you want.
* [Local python venv](#local-environment)
* [Docker](#docker-environment)
* [AWS Serverless](#aws-serverless) (Still under Development)
* [React Native](#react-native) (Still under Development)
* [Desktop Native](#desktop-native) (Still under Development)

## Local Environment

> To create and develop a local application we are using [virtualenv](https://pypi.org/project/virtualenv/). A tool for creating isolated virtual python environments.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
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
```shell
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
    * Go to: [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
* "Windows-Key + R" will show you the 'RUN' box
    * Type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

docker build -t flask_app:latest .
docker run -p 5000:5000 flask_app

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

systemctl start docker

```
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

docker build -t flask_app:latest .
docker run -it -p 5000:5000 flask_app

```

## AWS Serverless

> **Note:** Still under development

> To create and deploy a serverless application we are using [The Serverless Framework](https://www.serverless.com/) whice allows for a zero-friction serverless development, allowing you to easily build apps that auto-scale on low cost, next-gen cloud infrastructure.
> 
> The Serverless framework is an open source tool that provides an easy YAML + CLI development and deployment to AWS, Azure, Google Cloud, Knative & more.

## Via npm
* Open browser and install node.js:
    * Go to: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
npm update -g serverless

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
npm update -g serverless
```

## Via terminal/console

### Windows
* Open browser and install Chocolatey: 
    * Go to: [https://chocolatey.org/install](https://chocolatey.org/install) to get the installer
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
choco install serverless

```

> **Note:** if the package does not install you may need to run the comand as an admin.
> 
> press the  "Windows-Key" type "cmd", "Right-Click" on the word "Command Prompt" and Select the option "Run as administrator" and then follow the previous steps again

* Open browser and install docker desktop:
    * Go to: [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
* "Windows-Key + R" will show you the 'RUN' box
    * Type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal

```shell
serverless

cd <Path To>/my_awesome_project

sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-wsgi

serverless deploy

```

* Open browser and install Chocolatey from the 
    * Go to: [https://app.serverless.com/](https://app.serverless.com/) to see the deployed application

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
curl -o- -L https://slss.io/install | bash

```

* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

systemctl start docker

cd <Path To>/my_awesome_project

sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-wsgi

serverless deploy

```

* Open browser and go to: [https://app.serverless.com/](https://app.serverless.com/) to see the deployed application

## React Native

> For native mobile apps we are useing; react natve, specifically we are using [expo](https://expo.io/) a framework and a platform for universal React applications. It is a set of tools and services built around React Native and native platforms that help you develop, build, deploy, and quickly iterate on iOS, Android, and web apps from the same JavaScript/TypeScript codebase.

> Advantages include faster build and testing workflows/processes, remote testing while developing with Over The Air (OTA) updates with changes visible on save during development.

> However there are some disadvantages and [Limitations](https://docs.expo.io/introduction/why-not-expo/) Expo is aware of these and describes them quite well. we suggest reviewing these limitations beforee using our pre-built method.

> Build one project that runs natively on all your users' devices.

* Open browser and install node.js:
    * Go to: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
    * Follow the installation instructions and then continue to the next steps

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g expo-cli

npm install

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g expo-cli

npm install

```

### Changing the App URL

> Because Flask BDA does not dictate where you should host your website, you will need to tell your Mobile App where to go.

> In the quickstart example we created a project called `"My Awesome Project"`, however, you may have called the project something else.
> This would have created a folder where the name is all in lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`.

> For mobile we will have automaticallyed created a seperate `"_mobile_app"` folder where the prefix of the folder is your project name eg `my_awesome_project_mobile_app`. This is to prevent issues with Serverless and allow you to not have to deploy all the code for a mobile app onto your web-server.

* Open the Mobile App folder `my_awesome_project_mobile_app`
    * Once open, select the `app.json` file and edit line 2 `"server_base_url": "https://github.com/RyanJulyan/Flask-BDA"` by replacing `https://github.com/RyanJulyan/Flask-BDA` with your own server name.

### Run App
* Install the `expo` App on your own mobile phone by searching for "expo" on the Apple or Google Play Store:
    * `iOS` Go to: [https://apps.apple.com/app/apple-store/id982107779](https://apps.apple.com/app/apple-store/id982107779)
    * `Android` Go to: [https://play.google.com/store/apps/details?id=host.exp.exponent](https://play.google.com/store/apps/details?id=host.exp.exponent)

> Once you have the app installed on your phone you can start a development server on your local machine.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

expo start

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

expo start

```

> This will open a webpage with a QR code on it. This will allow you to use the Expo app if you are on Andriod or use the camera if you are on iOS to scan the code and open your app directly from the development server.

> **Note** if you wish for people not on your network to be able to scan and test the App remotely; press the `tunnel` tab button above the QR code.

### Deploying to stores
* Open browser and review expo's recomendations to ensure you are ready to deploy:
    * Go to:https://docs.expo.io/distribution/app-stores/
* Open browser and review expo's recomendations on building for the different platforms:
    * Go to:https://docs.expo.io/distribution/building-standalone-apps/

> Part of the reccomendations is to ensure that images are optimized. To do this expo have reccomended the [expo-optimize package](https://github.com/expo/expo-cli/tree/master/packages/expo-optimize#-welcome-to-expo-optimize) which can assist with optimizing images. Optimizing images can noticeable improve your native app TTI (or time-to-interaction) which means less time on splash screens and quicker delivery over poor network connections

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g sharp-cli

npx expo-optimize --quality 0.9

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g sharp-cli

npx expo-optimize --quality 0.9

```

## Desktop Native

> To create and develop a desktop application we are using [flaskwebgui](https://github.com/ClimenteA/flaskwebgui). A tool for creating and running your flask web application in a chrome wrapper.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install virtualenv
virtualenv venv

venv\Scripts\activate

pip install --no-cache-dir -r requirements.txt

python run_desktop.py

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install virtualenv
virtualenv venv

venv/bin/activate

pip install --no-cache-dir -r requirements.txt

python run_desktop.py

```

> This will open a maximized window that will run like a normal desktop application. This will use the locally installed chrome browser to serve the content.

> By default this application will be served on port `7000`, if that conflicts with any existing applications, you can edit the port in the `run_desktop.py` file.

# Installing Additional Python Packages

> If you include additional python packages in your project don't forget to run a `pip freeze` from your terminal to ensure you get that correct packages for your deployments

```shell
pip freeze > requirements.txt

```

> **Note** It is suggested that you install and freeze Additional Python Packages from a virtual environment rather than globally. This keeps your `requirements.txt` small and limited to the packes you are using in your specific project.

# OpenAPI/Swagger API

> Flask BDA uses [SwaggerUI](https://swagger.io/tools/swagger-ui/) by default to assist and present the API to a user/client.

> SwaggerUI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption.

To Access the SwaggerUI:
* Go to your browser and insert the URL `<base_URL>/api/docs` to access the SwaggerUI Api eg: [`http://localhost:5000/api/docs`](http://localhost:5000/api/docs)

# Import API to Postman

> Many developers will prefer [Postman](https://www.postman.com/) over [SwaggerUI](https://swagger.io/tools/swagger-ui/) to test and integrate API's with their code. We have assisted by providing a direct collection export for Postman.

> To import the collection on Postman:
* Ensure you have downloaded and installed [Postman](https://www.postman.com/downloads/)
* Once installed, click on file (on the top left of the application menu bar)
* Choose `Import...` (CTRL+O)
* Select `Link` from the Tabs
* Insert the URL `<base_URL>/api/postman` eg: [`http://localhost:5000/api/postman`](http://localhost:5000/api/postman)
* Press `Continue`
* This will show you the nameof the API as defined in the API config
* Review and click `Import`

> This will import a postman collection which will become availible on the left hand side as a folder (with sub folders from each of the endpoints you created).

> You can [generate code](https://learning.postman.com/docs/sending-requests/generate-code-snippets/) for many different [lanuages and frameworks](https://learning.postman.com/docs/sending-requests/generate-code-snippets/#supported-languagesframeworks) using Postamn. These Languages include but are not limited to:
* C
* C#
* Go
* Java
* Javascript
* Node
* PHP
* Python
* Powershell
* Ruuby
* Swift

> Allowing you to integrate your newly created API with existing projects


# External API Requests

> Sometimes you need to make external requests (eg to an external API). You could approach this by using [Ajax Requests](#ajax-requests), but sometimes you need to make these requests from the server side fore example if you want to automatically update currency conversions. When you want to access external API's through the server, you do not want to have to rely on a user actively being on the webpage to send the command, instead you want the server to be able to activate this comment. To acheive this we use the [requests module](https://www.w3schools.com/python/module_requests.asp).

* The structure of a requests is:
```python
import requests

requests.methodname(params)
```

### Get Request Method
```python
import requests

params = {"model": "Mustang"}

x = requests.get('https://w3schools.com/python/demopage.php', params = params)
print(x.status_code)
print(x.text)
```

### Post Request Method
```python
import requests

data = {"Name":"Example"}
headers = {"Authorization": "Bearer <token>"}

x = requests.post('https://w3schools.com/python/demopage.php', data = data, headers = headers)
print(x.status_code)
print(x.text)
```

### Delete Request Method
```python
import requests

x = requests.delete('https://w3schools.com/python/demopage.php')
print(x.status_code)
print(x.text)
```

# Ajax Requests

> Ajax requests, typically an HTTP request made by (browser-client) in Javascript that uses XML/JSON to request data and/or response data from either an internal or external system. Ajax requests are made using [</> htmx](https://htmx.org/) by default.

> htmx is a dependency-free library that allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext. For a details on how to use htmx, please refer to the [docs](https://htmx.org/docs/) and for a full reference on the functionality, please refer to: [https://htmx.org/reference/](https://htmx.org/reference/)

You can use htmx to implement many common UX patterns, such as Active Search:
```html
<input type="text" name="q" 
    hx-get="/trigger_delay" 
    hx-trigger="keyup changed delay:500ms" 
    hx-target="#search-results" 
    placeholder="Search..."/>

<div id="search-results"></div>
```
This input named q will issue a request to `/trigger_delay` 500 milliseconds after a key up event if the input has been changed and inserts the results into the div with the id search-results.

# Testing

> Testing is a vital part to ensuring a project runs successfully

There are 3 aspects of testing provided in Flask BDA:
* CI/CD through [Github actions workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions) which is already set up to implement but can also be used independently from GitHub:
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
```shell
cd <Path To>/my_awesome_project

venv\Scripts\activate

flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=11 --max-line-length=127 --statistics

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
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
```shell
cd <Path To>/my_awesome_project

venv\Scripts\activate

python -m unittest discover

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
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
    * Responsive layouts
    * Mobile specific views
    * SEO ready page index template file
    * Isolated module code and templates
    * Configuration file `config.py` for quick access and management of environment and environment variables and default SEO
    * Debugging built in and accessable through the Configuration file `config.py`
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
    * URL's (prefixed by the module name and replace xyz in the below details)
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
└── `project_name`
       ├── .github
       │    └── workflows
       │          ├── docker-image.yml
       │          └── run_tests.yml
       ├── app
       │    ├── mod_audit
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     └── models.py
       │    ├── mod_auth
       │    │     ├── templates
       │    │     │     ├── mobile
       │    │     │     │    └── auth
       │    │     │     │         ├── admin
       │    │     │     │         │    ├── create.html
       │    │     │     │         │    ├── edit.html
       │    │     │     │         │    ├── index.html
       │    │     │     │         │    └── show.html
       │    │     │     │         └── public
       │    │     │     │              └── public_list.html
       │    │     │     └── auth
       │    │     │          ├── admin
       │    │     │          │    ├── create.html
       │    │     │          │    ├── edit.html
       │    │     │          │    ├── index.html
       │    │     │          │    └── show.html
       │    │     │          └── public
       │    │     │               └── public_list.html
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     ├── forms.py
       │    │     └── models.py
       │    ├── mod_email
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     └── models.py
       │    ├── mod_file_upload
       │    │     ├── templates
       │    │     │    └── file_upload
       │    │     │         └── upload.html
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
       │    │     ├── mobile
       │    │     ├── public
       │    │     ├── 403.html
       │    │     ├── 404.html
       │    │     └── index.html
       │    └── __init__.py
       ├── create_module_template
       │    ├── generated_config
       │    │     └── models
       │    │          └── xyz
       │    │               └── models.json
       │    └── mod_xyz
       │          ├── templates
       │          │     ├── mobile
       │          │     │    └── `projects`
       │          │     │         ├── admin
       │          │     │         │    ├── create.html
       │          │     │         │    ├── edit.html
       │          │     │         │    ├── index.html
       │          │     │         │    └── show.html
       │          │     │         └── public
       │          │     │              └── public_list.html
       │          │     └── `projects`
       │          │          ├── admin
       │          │          │    ├── create.html
       │          │          │    ├── edit.html
       │          │          │    ├── index.html
       │          │          │    └── show.html
       │          │          └── public
       │          │               └── public_list.html
       │          ├── api_controllers.py
       │          ├── controllers.py
       │          ├── forms.py
       │          └── models.py
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

## Low-code platform
### Definition
> A low-code development platform provides a development environment used to create application software through programatic or graphical user interfaces and configuration instead of traditional hand-coded computer programming.

# License

## Python 3

View license information for Python 3. (https://docs.python.org/3.8/license.html) and other legal agreements (https://www.python.org/about/legal/)

________________________________________

## Docker

View license information for Docker. (https://www.docker.com/legal/components-licenses) and other legal agreements (https://www.docker.com/legal)

As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc from the base distribution, along with any direct or indirect dependencies of the primary software being contained).

Some additional license information which was able to be auto-detected might be found in the repo-info repository's python/ directory.

As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses for all software contained within.

________________________________________

## Serverless Framework

View license information for Serverless Framework and other legal agreements (https://app.serverless.com/legal/terms).

________________________________________

## Expo Framework

View license information for the Expo Framework and other legal agreements (https://github.com/expo/expo/blob/master/LICENSE).

It is the user's responsibility to ensure that adhere to the Acceptable Use Policy (https://app.serverless.com/legal/aup)

________________________________________

## The Flask-BDA License

Flask-BDA is created and distributed under the developer-friendly Flask-BDA License. The Flask-BDA License is derived from the popular Apache 2.0 license.

The Flask-BDA License is the legal requirement for you or your company to use and distribute Flask-BDA and derivative works such as the applications you make with it. Your application or project can have a different license, but it still needs to comply with the original one.

### The license grants you the following permissions:
* You are free to commercialise any software created using original or modified (derivative) versions of Flask-BDA
* You are free to commercialise any plugin, extension or tool created for use with Flask-BDA
* You are free to modify Flask-BDA and you are not required to share the changes
* You are free to distribute original or modified (derivative) versions of Flask-BDA
* You are given a license to any patent that covers Flask-BDA

### The license prevents you from doing the following:
* You can not commercialise original or modified (derivative) versions of the Flask-BDA editor and/or engine
* You can not hold Flask-BDA or Ryan Julyan liable for damages caused by the use of Flask-BDA
* You can not bring any warranty claims to Flask-BDA or Ryan Julyan
* You can not use the Flask-BDA trademark unless express permission has been given (see exceptions and additional information)
The license requires that you do the following:
    * You must include the Flask-BDA license and copyright notice in any work you create
    * You must state significant changes made to Flask-BDA

License and copyright notice inclusion

The Flask-BDA License requires that you must include the license and copyright notice with all copies of Flask-BDA and in any derived work created using Flask-BDA. It is up to you to decide how you wish to distribute the license and notice. Below are some examples of how this can be done:
* Show the license and notice at the end of a credits screen if your application has one
* Show the license and notice from a dedicated license screen or popup in your application
* Print the license and notice to an output log when your application starts
* Put the license and notice in a text file and include it with the distribution of your application
* Put the license and notice in a printed manual included with your application

________________________________________

Copyright 2021 Flask-BDA, Ryan Julyan
Licensed under the Flask-BDA License version 0.1 (the "License"); you may not use `Flask-BDA` except in compliance with the License.
You may obtain a copy of the [License](https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE), at
[`https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE`](https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE)
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
