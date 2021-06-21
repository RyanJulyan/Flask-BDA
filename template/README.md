# Flask-BDA
Flask-BDA is built using a Flask Rapid Application Development (RAD) called [Flask-BDA](https://github.com/RyanJulyan/Flask-BDA/).

# Know how to style a MD document properly
[https://www.markdownguide.org/basic-syntax/](https://www.markdownguide.org/basic-syntax/)

# Requirements
* Download and install [Python](https://www.python.org/downloads/) (suggested 3.8.6) if you do not already have it installed.
    * Ensure pip is installed (pip should be installed already because it comes with the latest versions of python) in case it is not, please install it from here: https://pip.pypa.io/en/stable/installing/
        * To check if pip is installed you can run the following command in your terminal
```shell
python -m pip --version
```

# Quickstart

> To get started building your first project, with Flask-BDA, follow the simple steps below to create your own pre-configured development environment up and running in minutes.

> In this quickstart we are going to create a project called `"My Awesome Project"`, however, you can call the project anything you want.

* Ensure you have installed the [requirements](#requirements)

### Windows
* Open a new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
    * Please ensure you put quotes around your project name to prevent errors eg: `"My Awesome Project"`
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project"

```

### Linux / Mac
* Open a new terminal
    * "Control + Option + Shift + T" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
    * Please ensure you put quotes around your project name to prevent errors eg: `"My Awesome Project"`
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project"

```
---

> **Note:** If you did not fill in a valid project name you will get prompted to do so:
> * Fill in your project name when prompted eg:
>    * Please ensure you put quotes around your project name to prevent errors eg: `"My Awesome Project"`
```python
Invalid Project Name!
Please enter a valid project name!
"My Awesome Project"
```
> **Note:** You will notice this creates a folder in the same path as the file: "create_project_git.py".
> This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`

> **Note:** During development, you may wish to use another branch or repo entirely. This can help with testing, or if you have broken away from the core Flask-BDA prooject.
> * You can specify the `Owner`, `Repo` and `Branch` when you create a new project.
```python
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/RyanJulyan-Dev/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project" --owner="RyanJulyan" --repo="Flask-BDA" --branch="RyanJulyan-Dev"

```

# Update Database

> **Note:** Still to be tested for all connection types!

> Database connections are quick and easy in Flask-BDA. You can have 1 or multiple databases, and different tenants can have their own database connections as well as their own database type (SQLite, MySQL, SQL Server, PostgreSQL)

> By default, Flask-BDA has a SQLite database set up. This is really because then you do not require addtional infistructure to set it up and get going, so makes SQLite a fast and easy choice.

## MySQL
To change the default database:
* Create a new MySQL Database (`flaskbda`), User (`flaskbda_user`) and Password (`password`)
* Open the file `config.py`
* Comment out the `DATABASE_ENGINE` for SQLite, and comment in the mysql `DATABASE_ENGINE`.
* Comment out the `DATABASE_NAME` for SQLite, and comment in the mysql:
    * `DATABASE_HOST`
    * `DATABASE_PORT`
    * `DATABASE_USERNAME`
    * `DATABASE_PASSWORD`
    * `DATABASE_NAME`
* Comment out the `SQLALCHEMY_DATABASE_URI` for SQLite, and comment in the mysql `SQLALCHEMY_DATABASE_URI`.

```python

##########
# SQLite #
##########
# DATABASE_ENGINE = 'sqlite:///'
# DATABASE_NAME = os.path.join(BASE_DIR, 'databases/sqlite/default.db')

# SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_NAME

#########
# MySQL #
#########
DATABASE_ENGINE = 'mysql://'
DATABASE_HOST = ''
DATABASE_PORT = '1433'
DATABASE_USERNAME = ''
DATABASE_PASSWORD = ''
DATABASE_NAME = ''

SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + ':' + DATABASE_PORT + '/' + DATABASE_NAME


```

* You will then need to update the database connection details with your own details:
    * `DATABASE_HOST`
    * `DATABASE_PORT`
    * `DATABASE_USERNAME`
    * `DATABASE_PASSWORD`
    * `DATABASE_NAME`

```python
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'
DATABASE_USERNAME = 'flaskbda_user'
DATABASE_PASSWORD = 'password'
DATABASE_NAME = 'flaskbda'

```

## SQL Server
To change the default database:
* Create a new MySQL Database (`flaskbda`), User (`flaskbda_user`) and Password (`password`)
* Open the file `config.py`
* Comment in the SQLServer `import pyodbc`.
* Comment in the SQLServer `DATABASE_DRIVER`.
* Comment out the `DATABASE_ENGINE` for SQLite, and for example comment in the SQLServer `DATABASE_ENGINE`.
* Comment out the `DATABASE_NAME` for SQLite, and comment in the SQLServer:
    * `DATABASE_HOST`
    * `DATABASE_PORT`
    * `DATABASE_USERNAME`
    * `DATABASE_PASSWORD`
    * `DATABASE_NAME`
* Comment out the `SQLALCHEMY_DATABASE_URI` for SQLite, and comment in the `try` and `except` for the SQLServer `SQLALCHEMY_DATABASE_URI`.

> **Note:** if you are running and trying to connect to `SQLEXPRESS`. please comment in the SQLServer `SQLEXPRESS`. This will be handeled in the `try` and `except` to create the correct `SQLALCHEMY_DATABASE_URI`

> **Note:** if you are want  windows authentication. please comment in the SQLServer `TRUSTED_CONNECTION`. This will be handeled in the `try` and `except` to create the correct `SQLALCHEMY_DATABASE_URI`


```python

##########
# SQLite #
##########
# DATABASE_ENGINE = 'sqlite:///'
# DATABASE_NAME = os.path.join(BASE_DIR, 'databases/sqlite/default.db')

# SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_NAME

#############
# SQLServer #
#############
import pyodbc   # noqa: E402
DATABASE_ENGINE = 'mssql+pyodbc://'
# SQLEXPRESS = '\\SQLEXPRESS'  # for SQLEXPRESS
# TRUSTED_CONNECTION = 'yes'  # for windows authentication.
DATABASE_DRIVER = 'SQL+Server+Native+Client+11.0'  # for windows authentication.
DATABASE_HOST = ''
DATABASE_PORT = '1433'
DATABASE_USERNAME = ''
DATABASE_PASSWORD = ''
DATABASE_NAME = ''

try:
    if SQLEXPRESS == '\\SQLEXPRESS':
        try:
            if TRUSTED_CONNECTION == 'yes':
                SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_HOST + ':' + DATABASE_PORT + SQLEXPRESS + '/' + DATABASE_NAME + '?trusted_connection=' + TRUSTED_CONNECTION + '&driver=' + DATABASE_DRIVER
            else:
                SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + ':' + DATABASE_PORT  + SQLEXPRESS + '/' + DATABASE_NAME + '&driver=' + DATABASE_DRIVER
        except NameError:
            SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + ':' + DATABASE_PORT  + SQLEXPRESS + '/' + DATABASE_NAME + '&driver=' + DATABASE_DRIVER
except NameError:
    try:
        if TRUSTED_CONNECTION == 'yes':
            SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_HOST + ':' + DATABASE_PORT + '/' + DATABASE_NAME+ '?trusted_connection=' + TRUSTED_CONNECTION + '&driver=' + DATABASE_DRIVER
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + ':' + DATABASE_PORT  + SQLEXPRESS + '/' + DATABASE_NAME + '&driver=' + DATABASE_DRIVER
    except NameError:
        SQLALCHEMY_DATABASE_URI = DATABASE_ENGINE + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + ':' + DATABASE_PORT + '/' + DATABASE_NAME + '&driver=' + DATABASE_DRIVER


```

* You will then need to update the database connection details with your own details:
    * `DATABASE_HOST`
    * `DATABASE_PORT`
    * `DATABASE_USERNAME`
    * `DATABASE_PASSWORD`
    * `DATABASE_NAME`

```python
DATABASE_HOST = 'MSSQLSERVER'
DATABASE_PORT = '1433'
DATABASE_USERNAME = 'flaskbda_user'
DATABASE_PASSWORD = 'password'
DATABASE_NAME = 'flaskbda'

```

Ensure that your MS-SQL instance has remote connection rights set up and enabled reference (here)[https://knowledgebase.apexsql.com/configure-remote-access-connect-remote-sql-server-instance-apexsql-tools/]:
* Right – click on the server 
* Select the Properties option.
    * In the Server Properties dialog select the Connections tab (on the left)
        * Check the "Allow remote connections to this server" checkbox

Ensure that the "SQL server configuration management" settings are configured correctly
* Start-> Programs -> Microsoft SQL Server <Version eg: 2019>
    * Select "SQL Server Configuration Manager"
        * In the left pane of SQL Server Configuration Manager select the "SQL Server Network Configuration"
            * select Protocols for <your server name eg: MSSQLSERVER>
                * Make sure that TCP/IP protocol is enabled and right click on TCP/IP and select the Properties option. In the TCP/IP Properties dialog select the IP Addresses tab and scroll down to IPAII. If the TCP Dynamic Ports dialog box contains 0, which indicates that the Database Engine is listening on dynamic ports, delete the 0 and set the TCP Dynamic Ports to blank and TCP Port to 1433. Port 1433 is the default instance that SQL Server uses.
                * When you click the OK button you will be prompted with a message to restart the service
* In the left pane of SQL Server Configuration Manager select "SQL Server Services"
    * right-click SQL Server<instance_name eg: MSSQLSERVER>
        * click Restart

# Multi Tenants

> By default Flask-BDA connects to a tenant called `core`. this is done using the `SQLALCHEMY_BINDS` object which should have the specific connection details you require for each tenant. By default the above default connection details are combined into a string called `SQLALCHEMY_DATABASE_URI` which was meant to allow for quick and easy single tenant setup.

> You can use this same structure however to have multiple tenants quickly. To add a new tenant, simply:
* Create a new line in the  `SQLALCHEMY_BINDS` object, with the name of the tenant and the connection string details
    * Remember to create the database before trying to connect to it.
    * The database connection types do not have to be the same per tenant in the same application (meaning different tenants can use different databases)

```python
SQLALCHEMY_BINDS = {
    "core": SQLALCHEMY_DATABASE_URI,
    "client1": 'sqlite:///databases/sqlite/client1.db',
}

```

> You can now interact with an isolated tenant database by adding the argument `organization=` to your url eg:
`example.com?organization=client1` where `client1` is the name that you added in the `SQLALCHEMY_BINDS` object.

# Create new [CRUD](#crud) module

> A module is a self-contained component, making it easier to manage as the program grows. Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views
> 
> When you create a new CRUD module, all the elements from the folder `create_module_template` are copied into the app directory and renamed to the module name you provide by replacing all `xyz` values with your module name and adding additional data model information as described below

## How to create a new module

* To create your own custom modules, Open and run the file: `<Path To>/<my_awesome_project>/create_module_json.py`
    * Fill in the instructions eg:
```python
cd <Path To>/<my_awesome_project>/

python create_module_json.py --module=Projects

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
Does name have a Relationship with another Data Model? ('True', 'False'): False
Default value: 

```

> **Note:** This will keep looping until you type and submit the exact words: "STOP_CREATING_FIELDS". 
> 
> This allows you to create multiple fields for your module quickly and easily.

* Try create a few more fields like:
    * "Start Date" as a 'Date' field type
    * "Budget" as a 'Float'
    * "Status" as an 'Enum' with the options: 'Pitch', 'Active' and 'Completed'

> The above fields should show you have different feild types interact and how you can create multiple fields.

> **Note:** Relationships will always be made on the `id` of the model provided.
> 
> A ForeignKey is created on the field, as well as a lazy relationship between the model provided `id` field

* When you have finished creating all the fields you want to create type and submit the words: "STOP_CREATING_FIELDS". 
```python
Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): STOP_CREATING_FIELDS

```
* You will then be propted if you would like to create this module logic from the data model. Generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input. if you want to create all the views type and submit "True"
```python
Create module logic from Data Model? ('True', 'False'): True

```

> **Note:** you can also generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input to do this you can, Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * Fill in the instructions eg:
```python
cd <Path To>/<my_awesome_project>/

python create_module.py --module=projects

```

This will then create the required files and folders as described below in the [App changes](#app-changes)

### App changes

> Files and folders from the `create_module_template` folder are created for the `Projects` module, and then added to the `app` folder
>
> This will create a scaffolded admin panel views, an API, and public-facing views and logic to allow you to immediately interact with the module you created.
> 
> From the admin panel you will be able to perform the following actions: Create, Read, Update, and Delete ("CRUD") for your new module.
> 
> The public-facing views allows guest users (users not logged in) to see a view of the information provided

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
* [Shared Hosting](#shared-hosting) (Still Testing)
* [Docker](#docker-environment)
* [AWS Serverless](#aws-serverless) (Still under Development)
* [React Native](#react-native) (Still under Development)
* [Desktop Native](#desktop-native)

## Local Environment

> To create and develop a local application we are using [virtualenv](https://pypi.org/project/virtualenv/). A tool for creating isolated virtual python environments.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install --upgrade pip
pip install virtualenv
virtualenv venv

venv\Scripts\activate

pip install --upgrade pip
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

pip install --upgrade pip
pip install virtualenv
virtualenv venv

source venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development

flask run

```

## Shared Hosting

> Some shared hosting services offer the ability to run python applications on their servers. I personally have used [A2hosting](http://www.a2hosting.com/refer/171923) their support has been amazing and the price to features are one of the best I have come accross.

> **Note:** You are not limited to A2 as a shared hosting option, this is however where I have tested Flask-BDA and have my experience in uploading and running a shared hosting option. If your shared hosting option offers a similar set of features please feel free to use them.

> For A2 you will need to set up your server to run a python application which may require some configuration for [example](https://www.a2hosting.co.za/kb/developer-corner/python/installing-and-configuring-flask-on-linux-shared-hosting).

> To get your custom application to work:
* You will first need to upload your files (I find this easiest to zip and then upload them to the required location).
* Unzip them on the server and ensure they are in the folder location you require
* Log in to cPanel again to update the python configuration
    * Click the `Setup Python App` again
    * Edit the existing application
    * Change the `Application startup file` to `run_shared_server.py`
    * Restart the server and your application should now be working as expected.

## Docker Environment

> To create and deploy a containerized application we are using [Docker](https://www.docker.com/) which helps developers and development teams build and ship apps. Docker is used for the building and sharing of containerized applications and microservices.

> **Note:** If you are using [Github](https://github.com/) and have docker installed (details on how to install later in the documentation), you will get a new image built every time you `push` or do a `pull_request` on Github, which is set up in the file: `docker-image.yml` however if you want to do this manually, please follow the steps below:

### Windows
* Open a browser and install docker desktop
    * Go to: [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
* "Windows-Key + R" will show you the 'RUN' box
    * Type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open a new terminal
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

> To create and deploy a serverless application we are using [The Serverless Framework](https://www.serverless.com/) which allows for a zero-friction serverless development, allowing you to easily build apps that auto-scale on low cost, next-gen cloud infrastructure.
> 
> The Serverless framework is an open-source tool that provides an easy YAML + CLI development and deployment to AWS, Azure, Google Cloud, Knative & more.

> **Note:** You may need to adjust the defult database strings before del=polying as serverless does not support "SQLite" as the function does not keep state.
> 
> To update the database strings, please refer to: [Config]

## Via npm
* Open browser and install node.js:
    * Go to: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

### Windows
* Open a new terminal
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
* Open a browser and install Chocolatey: 
    * Go to: [https://chocolatey.org/install](https://chocolatey.org/install) to get the installer
* Open a new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
choco install serverless

```

> **Note:** If the package does not install you may need to run the command as an admin.
> 
> press the  "Windows-Key" type "cmd", "Right-Click" on the word "Command Prompt" and select the option "Run as administrator" and then follow the previous steps again

* Open a browser and install docker desktop:
    * Go to: [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
* "Windows-Key + R" will show you the 'RUN' box
    * Type "C:\Program Files\Docker\Docker\Docker Desktop.exe" to open docker
* Open a new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal

```shell
serverless

cd <Path To>/my_awesome_project

sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-wsgi

serverless deploy

```

* Open a browser and install Chocolatey from the 
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

* Open a browser and go to: [https://app.serverless.com/](https://app.serverless.com/) to see the deployed application

## React Native

> For native mobile apps we are using react native, specifically we are using [expo](https://expo.io/) a framework and a platform for universal React applications. It is a set of tools and services built around React Native and native platforms that help you develop, build, deploy, and quickly iterate on iOS, Android, and web apps from the same JavaScript/TypeScript codebase.

> Advantages include faster build and testing workflows/processes, remote testing while developing with Over The Air (OTA) updates with changes visible on save during development.

> However there are some disadvantages and [Limitations](https://docs.expo.io/introduction/why-not-expo/) Expo is aware of these and describes them quite well. we suggest reviewing these limitations before using our pre-built method.

> Build one project that runs natively on all your users' devices.

* Open a browser and install node.js:
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

> For mobile we will have automatically created a separate `"_mobile_app"` folder where the prefix of the folder is your project name eg `my_awesome_project_mobile_app`. This is to prevent issues with the `Serverless` configuration `package.json` and allow you to not have to deploy all the code for a mobile app onto your web server.

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

> This will open a webpage with a QR code on it. This will allow you to use the Expo app if you are on Android or use the camera if you are on iOS to scan the code and open your app directly from the development server.

> **Note:** if you wish for people not on your network to be able to scan and test the App remotely; press the `tunnel` tab button above the QR code.

### Deploying to stores
* Open browser and review expo's recommendations to ensure you are ready to deploy:
    * Go to:https://docs.expo.io/distribution/app-stores/
* Open browser and review expo's recommendations on building for the different platforms:
    * Go to:https://docs.expo.io/distribution/building-standalone-apps/

> Part of the recommendations are to ensure that images are optimized. To do this expo has recommended the [expo-optimize package](https://github.com/expo/expo-cli/tree/master/packages/expo-optimize#-welcome-to-expo-optimize) which can assist with optimizing images. Optimizing images can noticeable improve your native app TTI (or time-to-interaction) which means less time on splash screens and quicker delivery over poor network connections

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

> To create and develop a desktop application we are using [flaskwebgui](https://github.com/ClimenteA/flaskwebgui). A tool for creating and running your flask web application in a chrome wrapper. To distribute the desktop application we are using [PyInstaller](http://www.pyinstaller.org/). PyInstaller freezes (packages) Python applications into stand-alone executables, under Windows, GNU/Linux, Mac OS X, FreeBSD, Solaris and AIX.

> Each deployment needs to be created on the specific platform that you wish to run it. As such we have created scripts that will allow you to manage these deployments, by placing the `build` and `dist` folders into parent folders for the respective platform. These folders will be prefixed with `desktop_` followed by the platform. This is done purly to allow you to manage the distribution and build processes for the specific platforms and not overwrite them when building on different platforms.

> To allow for the export to desktop to work correctly, we require some code changes. This is because by default Flask-BDA is intended for web and mobile development, and we have implemented a rate-limiter on the site. Unfortunately to rate limit, you require a server, and since you are exporting the system to a desktop application, it is not running a server.
>
> as such you need to remove all references to the limiter these can be found at `app/__init__.py`. To do this open the file in a text editor and comment out the following lines:
```python
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=app.config['DEFAULT_LIMITS']
# )

```

> **Note:** if you added custom limiter, search for `@limiter.limit` which would be found in your controllers. You will need to comment out all of those references and the import references e.g.: `from app import limiter`

> This will allow you to export the application as a desktop executable file without errors.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install --upgrade pip
pip install virtualenv
virtualenv venv

venv\Scripts\activate

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

python create_desktop_installer_windows.py

```

### Linux
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install --upgrade pip
pip install virtualenv
virtualenv venv

venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

python create_desktop_installer_lunix.py

```

### Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

pip install --upgrade pip
pip install virtualenv
virtualenv venv

venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

python create_desktop_installer_mac.py

```

> This will open a maximized window that will run like a normal desktop application. This will use the locally installed chrome browser to serve the content.

> By default this application will be served on port `7000`, if that conflicts with any existing applications, you can edit the port in the `run_desktop.py` file.

# Ajax Requests

> Ajax requests are made using [</> htmx](https://htmx.org/) by default
> htmx is a dependency-free library that allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext. For a details on how to use htmx, please refer to the [docs](https://htmx.org/docs/) and for a full reference on the functionality, please refer to: [https://htmx.org/reference/](https://htmx.org/reference/)

You can use htmx to implement many common UX patterns, such as Active Search:
```
<input type="text" name="q" 
    hx-get="/trigger_delay" 
    hx-trigger="keyup changed delay:500ms" 
    hx-target="#search-results" 
    placeholder="Search..."/>

<div id="search-results"></div>
```
This input named q will issue a request to `/trigger_delay` 500 milliseconds after a key up event if the input has been changed and inserts the results into the div with the id search-results.