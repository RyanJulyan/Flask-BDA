# Flask Business Driven App (BDA)
## Quickly create cross-platform, multi-tenant, SAAS-ready, mobile and web applications, and reactive web apps for any device. A Rapid Application Development (RAD) tool to assist with building flask python applications. Helping you build applications fast, right, and for the Future.

> **Note:** Still under Development!

# Status of the project
Current version: `0.0.0` Beta 

Flask-BDA is still under initial development and is being tested with [Python 3.8.6](https://www.python.org/downloads/release/python-386/) version.

> Current roadmap and high-level project plan: https://trello.com/b/uu4HNPBh/flask-bda-features-roadmap

Flask-BDA will follow semantic versioning for its releases, with a `{major}.{minor}.{patch}` scheme for versions numbers, where:

- major versions might introduce breaking changes
- minor versions usually introduce new features and might introduce deprecations
- patch versions only introduce bug fixes

Deprecations will be kept in place for at least 3 minor versions, after version `0.0.1`

# Overview
* [Status of the project](#status-of-the-project)
* [Why use Flask-BDA](#why-use-flask-bda)
* [Costs](#costs)
* [Process](#process)
* [Requirements](#requirements)
    * [Dependencies](#dependencies)
* [Quickstart](#quickstart)
    * [Update Database](#update-database)
    * [Multi Tenants](#multi-tenants)
    * [Create a new module](#create-a-new-module)
    * [Module Functionality](#module-functionality)
* [Update Database](#update-database)
* [Create new CRUD module](#create-new-crud-module)
* [Environments](#environments)
    * [Local Environment](#local-environment)
    * [Shared Hosting](#shared-hosting)
    * [Docker Environment](#docker-environment)
    * [AWS Serverless](#aws-serverless)
    * [React Native](#react-native)
    * [Desktop Native](#desktop-native)
* [Installing Additional Python Packages](#installing-additional-python-packages)
* [OpenAPI/Swagger API](#openapiswagger-api)
* [Import API to Postman](#import-api-to-postman)
* [External API Requests](#external-api-requests)
* [Ajax Requests](#ajax-requests)
* [Testing](#testing)
    * [Python flake8](#python-flake8)
    * [Python unittest](#python-unittest)
* [Features List](#features-list)
* [Project Structure](#project-structure)
* [Glossary](#glossary)
* [How can I help?](#how-can-i-help?)
* [License](#license)

# Why use Flask-BDA

> Other solutions such as [Tableau](https://www.tableau.com/), [Power BI](https://powerbi.microsoft.com/en-us/) and [Amazon QuickSight](https://aws.amazon.com/quicksight/), while fantastic tools, focus on reporting but do not let you edit or add data to the platforms when needed, meaning you require additional solutions or software to achieve your business goals

> Solutions like [Excel](https://www.microsoft.com/en-za/microsoft-365/excel) are accessible to everyone and give you all the flexibility you might need. Still, your data is scattered and does not easily allow for a shared source of truth for your team and clients, and it is very easy for excel documents to be out of sync or even shared, opening your company up to a security risk.

> Flask-BDA helps you by providing you with the control to deliver rapid, secure, Full-stack applications 2-5x (2-5 times) faster. With no vendor or environment lock-in, ever.

> [Flask](https://palletsprojects.com/p/flask/) is an open-source "micro-framework" written by Armin Ronacher that allows you to build web applications in Python. Shipping only a small core set of features provides an extensible base that allows developers to choose what additional tools they will need for their application.
>
> Despite being called a micro-framework, Flask is well suited to build small and large web applications. Flask has been used in production systems by large companies such as Twilio, Pinterest, Lyft, LinkedIn, and Uber.

> Flask-BDA helps you develop faster by providing you with a pre-existing flask application structure allowing you to:
> 
> Automatically deal with the tedious aspects that slow down software development
> * Create & manage all database connections and complex queries.
> * Application security with user and role-based access control
> * Automatic audits on every action

> Flask-BDA is a [low-code platform](#low-code-platform) (meaning we will help you by writing a lot of the code for you) that provides the tools for companies to rapidly develop and deploy secure applications that run on any device.
> 
> We change the way software is built so you can rapidly create and deploy critical applications of any size that evolve with your business saving you time & money.
> 
> Developers can build and deploy a full range of applications - from consumer apps to critical internal business systems - designed to help developers deliver secure applications quickly and efficiently, so apps are delivered in weeks and even days.
>
> Flask-BDA provides Full-stack development from; UI, business processes, custom logic, and data models to create cross-platform apps out of the box. Providing you with a scaffold that you can add your own custom code when needed. With no lock-in ever.
> 
> With pre-configured development environments, we reduce the pain (and cost) of getting to market, giving you the flexibility to choose where and how to deploy.

> Free and Developer-Friendly,
> Flask-BDA is a free-to-use, source available, application development tool with a developer-friendly [license](#license).

# Costs

> Flask-BDA is completely **FREE** to use for commercial and personal projects.

> However, Software development is always a costly exercise:
> * You will need to pay one or multiple Software Developers, Business Analysts, Designers, Project Managers, and other team members to build your product.
> * Your product is never finished. A software project will always need continued development.
>     * When you deliver a product, your competition is already working on new and improved features, and you need to be able to stay ahead or at least keep up, or users will move to your competition.
>     * Once you start using your product, you and your team will think of new features that will make it even better and improve your processes.
>     * Continued maintenance. As users use the product, they will find ways to break it that you haven't thought of, and they need to be fixed.

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

> With Flask-BDA, you **DON'T LOOSE ANY of the flexibility of "Normal Development"** as it uses standardized development patterns and tried and tested technologies.

> Flask-BDA uses many Open Source technologies and leverages existing technology stacks so that you can easily find other developers who use the same technologies. As a result, you do not have to pay for costly license fees or environment costs regardless of how much revenue your company makes or where you are in your business.

# Process

## Step 1:
### Download pre-configured development environment

> Start your with a quick and easy pre-configured development environment in minutes.

> No complex setup required. Only python (suggested [3.8.6](https://www.python.org/downloads/release/python-386/)) is required.

## Step 2:
### Update config and rapidly develop custom modules

> Upsdate your configurations: Database connections and application settings.

> Create your own modules and data structures (data model) allowing you to use different databases.

## Step 3:
### Fully functional pages

> Auto-generated fully functional:
> * `Admin` and `Mobile` pages
> * `REST APIs` with a Swagger front-end
> * `GraphQL API` with a GraphiQL front-end
> easily managed per module.

## Step 4:
### Customize

> Configure pages to your specific needs and easily share them with your team and clients.

> Write your own custom code in an isolated module, so you do not affect other modules, 

> Easily integrate modules accross different projects.

## Step 5:
### Deploy

> Use the same codebase to deploy to:
> * Desktop
> * Web
> * Mobile

> Environments include: 
> * Docker
> * AWS Serverless
> * Digital Ocean
> * Heroku
> * Shared hosting.

# Requirements
* Download and install [Python](https://www.python.org/downloads/) (suggested [3.8.6](https://www.python.org/downloads/release/python-386/)) if you do not already have it installed.
    * Ensure `pip` is installed (pip should be installed already because it comes with the latest versions of python) in case it is not, please install it from here: https://pip.pypa.io/en/stable/installing/
        * To check if pip is installed, you can run the following command in your terminal
```shell
python -m pip --version

```

> **NOTE:** This documentation assumes that you are running `pip3` as `pip`, as such all instructions are written with `pip`. If you would like to make `pip3` run when you call `pip`, from your tereminal, you can create a symlink to `pip3` from `pip`:

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you run the command as `sudo` eg: `sudo pip install --upgrade pip`
```shell
nano ~/.bash_profile

```
> In the file, paste the following:

```shell
alias pip='pip3'
alias python='python3'

```

> **NOTE:** You may need to remove python 2.7 on MacOS as it is pre-installed on my distributions this [like](https://newbedev.com/how-to-uninstall-python-2-7-on-a-mac-os-x-10-6-4) was very helpful to acheive this:

1) Remove the third-party Python 2.7 framework
```shell
sudo rm -rf /Library/Frameworks/Python.framework/Versions/2.7
```
2) Remove the Python 2.7 applications directory
```shell
sudo rm -rf "/Applications/Python 2.7"
```
3) Remove the symbolic links, in /usr/local/bin, that point to this Python version. See them using
```shell
ls -l /usr/local/bin | grep '../Library/Frameworks/Python.framework/Versions/2.7'
``` 
and then run the following command to remove all the links:
```shell
cd /usr/local/bin/
ls -l /usr/local/bin | grep '../Library/Frameworks/Python.framework/Versions/2.7' | awk '{print $9}' | tr -d @ | xargs rm
```

## Dependencies

> Once you have installed Python and `pip`, you will need to install a dependency for the Flask-BDA command line functions to run correctly:
```shell
pip install click

```

> Other Dependancies you may want to install globally (but should run automatically when you create a project) include:
```shell
pip install virtualenv
pip install flaskwebgui
pip install pyinstaller

```

# Quickstart

> To get started building your first project with Flask-BDA, follow the simple steps below to create your own pre-configured development environment up and running in minutes.

> In this quickstart, we will create a project called `"My Awesome Project"`. However, you can call the project anything you want.

* Ensure you have installed the [requirements](#requirements)

### Windows
* Open a new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
    * Please ensure you put quotes around your project name to prevent errors, e.g.: `"My Awesome Project"`
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project"

```

### Linux / Mac
* Open a new terminal
    * "Control + Option + Shift + T" to open the terminal
* Copy, paste and run the following code in the terminal
    * This will download the required `create_project.py` python file and run it to help you start a project
    * Please ensure you put quotes around your project name to prevent errors, e.g.: `"My Awesome Project"`
```shell
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/main/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project"

```
---

> **Note:** If you did not fill in a valid project name, you would get prompted to do so:
> * Fill in your project name when prompted, e.g.:
>    * Please ensure you put quotes around your project name to prevent errors, e.g.: `"My Awesome Project"`
```python
Invalid Project Name!
Please enter a valid project name:
"My Awesome Project"
```
> **Note:** You will notice this creates a folder in the same path as the file: "create_project_git.py".
> This folder will be lower case and will have stripped out all of the special characters and replaced spaces with underscores, e.g.: `my_awesome_project`

> **Note:** During development, you may wish to use another branch or repo entirely. This can help with testing or if you have broken away from the core Flask-BDA project.
> * You can specify the `Owner`, `Repo` and `Branch` when creating a new project.
```python
curl -L https://raw.githubusercontent.com/RyanJulyan/Flask-BDA/RyanJulyan-Dev/create_project_git.py --ssl-no-revok -o create_project_git.py

python create_project_git.py --project="My Awesome Project" --owner="RyanJulyan" --repo="Flask-BDA" --branch="RyanJulyan-Dev" --create_venv=True

```

# Update Database

> **Note:** Still to be tested for all connection types!

> Database connections are quick and easy in Flask-BDA. You can have 1 or multiple databases, and different tenants can have their own database connections as well as their own database type (SQLite, MySQL, SQL Server, PostgreSQL)

> By default, Flask-BDA has an SQLite database set up. This is really because you do not require additional infrastructure to set it up and get going, making SQLite a fast and easy choice.

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

> **Note:** if you are running and trying to connect to `SQLEXPRESS`. Please uncomment the SQLServer `SQLEXPRESS` variable. This will be handled in the `try` and `except` to create the correct `SQLALCHEMY_DATABASE_URI`

> **Note:** if you want windows authentication. Please uncomment the SQLServer `TRUSTED_CONNECTION` variable. This will be handled in the `try` and `except` to create the correct `SQLALCHEMY_DATABASE_URI`


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
* Right-click on the server 
* Select the Properties option.
    * In the Server Properties dialogue, select the Connections tab (on the left)
        * Check the "Allow remote connections to this server" checkbox

Ensure that the "SQL server configuration management" settings are configured correctly
> **NOTE:** Your installation will require `Client Tools Connectivity`, if you cannot find "SQL server configuration management", then you may need to modify your installation to include `Client Tools Connectivity`
> * if you cannot find the "" you may need to use the "Use the Computer Management"  tool instead. to access it.
>   * this seems to be a Windows 10 issue

* Start-> Programs -> Microsoft SQL Server <Version eg: 2019>
    * Select "SQL Server Configuration Manager"
        * In the left pane of SQL Server Configuration Manager, select the "SQL Server Network Configuration."
            * select Protocols for <your server name, e.g., MSSQLSERVER>
                * Make sure that TCP/IP protocol is enabled and right-click on TCP/IP, and select the Properties option. In the TCP/IP Properties dialogue, select the IP Addresses tab and scroll down to IPAII. If the TCP Dynamic Ports dialogue box contains 0, which indicates that the Database Engine is listening on dynamic ports, delete the 0 and set the TCP Dynamic Ports to blank and TCP Port to 1433. Port 1433 is the default instance that SQL Server uses.
                * When you click the OK button, you will be prompted with a message to restart the service
* In the left pane of SQL Server Configuration Manager, select "SQL Server Services."
    * right-click SQL Server<instance_name eg: MSSQLSERVER>
        * click Restart

# Multi Tenants

## Isolated Databases with the same functionality

> Multitenancy is a software architecture in which a single instance of software runs on a server and serves multiple tenants (clients). Multitenant software allows multiple independent instances of one or multiple applications operate in a shared environment.

> Flask-BDA supports veritically partitioned multi-tenancy. Vertical partitioning means that each tenant has a different database (and database connection string).

> By default, Flask-BDA connects to a tenant called `default`. This is done using the `SQLALCHEMY_BINDS` object (found in `config.py`), which should have the specific connection details you require for each tenant. The default connection details are combined into a string called `SQLALCHEMY_DATABASE_URI`, which was meant to allow for a quick and easy single tenant setup.

> You can use this same structure, however, to have multiple tenants you can quickly add them to the `SQLALCHEMY_BINDS` object. To add a new tenant, simply:
* Create a new line in the `SQLALCHEMY_BINDS` object, with the name of the tenant and the connection string details
    * Remember to create the database before trying to connect to it.
    * The database connection types (SQLite, MySQL, SQL Server, PostgreSQL) do not have to be the same. each tenant in the same application can have different connection types (meaning different tenants can use different databases and different engines)

```python
SQLALCHEMY_BINDS = {
    "default": SQLALCHEMY_DATABASE_URI,
    "client1": 'sqlite:///databases/sqlite/client1.db',
}

```

> You can now interact with an isolated tenant database by adding the argument `organization=` to your URL, e.g.:
`example.com?organization=client1` where `client1` is the name that you added in the `SQLALCHEMY_BINDS` object.

> This works by intercepting the `@app.before_request` in `app/_init_.py` and changing the db engine binding by using `db.choose_tenant(g.organization)` from the `app/mod_tenancy/multi_tenant.py` by using the global variable `g.organization` which gets set by fetching the URL argument `organization`. This allows the same code in the app, to be used by every tenant's database while keeping the data seperated.

## Interacting with different Databases in the same function

> Sometimes you need to interact with different databases in a single function (especially when integrating systems, or reading data from different sources).

> By default all controllers will have `MultiBindSQLAlchemy` imported. 
``` python
# import multiple bindings
from app.mod_tenancy.multi_bind import MultiBindSQLAlchemy

```
> Under the import there is commented out code intended to assist you with quickly implementing linking to different databases in a single function. Firstly the database binding needs to be added to the `SQLALCHEMY_BINDS` object. Reference the [Isolated Databases with the same functionality](#isolated-databases-with-the-same-functionality) to better understand how to add new databases to the `SQLALCHEMY_BINDS` object.

> You can then create a new object attached to the `db` object following the stucture of `db.<binding>` e.g.: `db.first` where `first` is the name you want to reference the binding in the rest of the code. You can then assign this variable to the `MultiBindSQLAlchemy` e.g.: `db.first = MultiBindSQLAlchemy('first')`.

> This now allows you to call custom code that will allow you to access the new database binding as well as the main tenant in a single function e.g.: `db.first.execute(...)`, where you can execute raw SQL code.

```python
db.first = MultiBindSQLAlchemy('first')
##################################################
## this will only work for the execute function ##
##################################################
db.first.execute(...)

```

> **Note: ** this will only work for the `execute` function, there are some advanced techniques to still use the SQLAlchemy ORM that can be found here: [SQLAlchemy execute tutorial](https://docs.sqlalchemy.org/en/14/core/tutorial.html)

# Create a new module

> A module is a self-contained component, making it easier to manage as the program grows. Modules in Flask-BDA help you create: a Data Model, Routes and associated functions for controlling the logic and Views.
> 
> When you create a new [CRUD](#crud) module, all the elements from the folder `create_module_template` are copied into the app directory and renamed to the module name you provide by replacing all `xyz` values with your module name and adding additional data model information as described below

## How to create a new module

* To create your own custom modules, Open and run the file: `<Path To>/<my_awesome_project>/create_module_json.py`
    * Where `<Path To>/<my_awesome_project>/` is the path to the project you created
    * Fill in the instructions, e.g.:
```python
cd <Path To>/<my_awesome_project>/

python create_module_json.py --module=Projects

```
* You can then create a table with columns by following the prompts, e.g.:
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
Does the name have a Relationship with another Data Model? ('True', 'False'): False
Default value: 

```

> **Note:** This will keep looping until you type and submit the exact words: "STOP_CREATING_FIELDS". 
> 
> This allows you to create multiple fields for your module quickly and easily.

* Try creating a few more fields like:
    * "Start Date" as a 'Date' field type
    * "Budget" as a 'Float'
    * "Status" as an 'Enum' with the options: 'Pitch', 'Active' and 'Completed'

> The above fields should show you have different field types interact and create multiple fields.

> **Note:** Relationships will always be made on the `id` of the model provided.
> 
> A ForeignKey is created on the field, as well as a lazy relationship between the model provided `id` field

* When you have finished creating all the fields you want to create, type and submit the words: "STOP_CREATING_FIELDS". 
```python
Create new field Name (type the string: 'STOP_CREATING_FIELDS' to exit): STOP_CREATING_FIELDS

```
* You will then be prompted if you would like to create this module logic from the data model. Generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input. if you want to create all the views, type and submit "True"
```python
Create module logic from Data Model? ('True', 'False'): True

```

> **Note:** you can also generate a module from a JSON file in "app/generated_config/models/<module>/models.json", where <module> is the name of the module you input to do this you can, Open and run the file: `<Path To>/<my_awesome_project>/create_module.py`
    * Where `<Path To>/<my_awesome_project>/` is the path to the project you created
    * Fill in the instructions eg:
```python
cd <Path To>/<my_awesome_project>/

python create_module.py --module=projects

```

This will then create the required files and folders as described below in the [App changes](#app-changes)

### App changes

> Files and folders from the `create_module_template` folder are created for the `Projects` module and then added to the `app` folder
>
> This will create a scaffolded admin CRUD views, a REST API (With Bulk Insert and Update), a GraphQL API, and public-facing views and logic to allow you to immediately interact with the module you created.
> 
> From the admin panel, you will be able to perform the following actions: Create, Read, Update, and Delete ("CRUD") for your new module.
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
                  │     │         │    └── show.html
                  │     │         └── public
                  │     │              └── public_list.html
                  │     └── `projects`
                  │          ├── admin
                  │          │    ├── create.html
                  │          │    ├── edit.html
                  │          │    ├── index.html
                  │          │    └── show.html
                  │          └── public
                  │               └── public_list.html
                  ├── api_controllers.py
                  ├── controllers.py
                  ├── forms.py
                  ├── models.py
                  └── types.py
```

# Module Functionality
> Creating a new module will provide you with 3 ways to interact with your new system `Public`, `Admin`, `REST API` and `GraphQL API`.

> To access these, they will require the app to be running on an [environment](#environments).

## Public View
> The `Public` view is a **non-authenticated** view of the data provided in the module.
### It can be accessed from (where `xyz` is the name of the module):
* `../xyz/`
    * Returns: [list elements]
    * Function name: `public_list`

## Admin View
> The `Admin` views are **authenticated** view of the data provided in the module.
### It can be accessed from (where `xyz` is the name of the module):
* `../admin/xyz/`
    * Type: View
    * Returns: [list elements]
    * Function name: `index`
* `../admin/xyz/create` 
    * Type: View
    * Returns: [single element]
    * Function name: `create`
* `../admin/xyz/store` 
    * Type: POST URL
    * Returns: [single element]
    * Function name: `store`
* `../admin/xyz/show/{id}`
    * Type: View
    * Returns: [single element]
    * Function name: `show`
* `../admin/xyz/edit/{id}`
    * Type: View
    * Returns: [single element]
    * Function name: `edit`
* `../admin/xyz/update/{id}`
    * Type: PUT URL
    * Returns: [single element]
    * Function name: `update`
* `../admin/xyz/destroy/{id}`
    * Type: DELETE URL
    * Returns: [single element]
    * Function name: `destroy`

## REST API
> The `API` views are a list of REST API endpoints, associated documentation and execution playground.

> Flask BDA uses [SwaggerUI](https://swagger.io/tools/swagger-ui/) to present the REST API to a user/client.

> SwaggerUI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. Instead, it’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with visual documentation making it easy for back-end implementation and client-side consumption.

To access the SwaggerUI:
* Go to your browser and insert the URL `<base_URL>/api/docs` to access the SwaggerUI REST API, e.g.: [`http://localhost:5000/api/docs`](http://localhost:5000/api/docs).

To access the REST API without SwaggerUI:
* Go to your browser or go to [postman](https://www.postman.com/) and insert the URL `<base_URL>/`
    *  `../api/xyz`
        * Method: GET
        * Returns: [list elements]
        * Function name: `XyzListResource` > `get`
    * `../api/xyz`
        * Method: POST
        * Returns: [single element]
        * Function name: `XyzListResource` > `post`
    * `../api/xyz/{id}`
        * Method: GET
        * Returns: [single element]
        * Function name: `XyzResource` > `get`
    * `../api/xyz/{id}`
        * Method: PUT
        * Returns: [single element]
        * Function name: `XyzResource` > `update`
    * `../api/xyz/{id}`
        * Method: DELETE
        * Returns: [single element]
        * Function name: `XyzResource` > `delete`
    * `../api/xyz/bulk`
        * Method: POST
        * Returns: [multiple elements]
        * Function name: `XyzBulkListResource` > `post`
    *  `../api/xyz/bulk`
        * Method: PUT
        * Returns: [multiple elements]
        * Function name: `XyzBulkListResource` > `update`
    * `../api/xyz/aggregate`
        * Method: GET
        * Returns: [single return, of multiple elements aggregated]
        * Function name: `XyzAggregateResource` > `get`

## GraphQL API
> The `graphql` views are a GraphiQL views, API endpoints, associated documentation and execution playground.

> Flask BDA uses [graphene-python](https://graphene-python.org/) and [GraphiQL](https://graphene-python.org/) to present the GraphQL API to a user/client, providing a simple but extendable API for making developers' lives easier.

> GraphQL is a data query language provides an alternative to REST and ad-hoc webservice architectures. 

To access the GraphiQL:
* Go to your browser and insert the URL `<base_URL>/graphql` to access the GraphiQL, GraphQL API, e.g.: [`http://localhost:5000/graphql`](http://localhost:5000/graphql).

To access the GraphQL API without GraphiQL:
* Go to your browser or go to [postman](https://www.postman.com/) and insert the URL `<base_URL>/`
    *  `../graphql`
        * Method: GET
        * Returns: [list elements]
        * Function name: `mod_graphql` > `query` > `Query` > `all_xyz`
    *  `../graphql`
        * Method: POST
        * Returns: [list elements]
        * Function name: `mod_graphql` > `mutation` > `Mutation` > `createXyz`


# Environments
There are currently 7 out of the box environments supported (with plans for more to be supported soon) with instructions on how to configure each for  `Windows / Linux / Mac`, and you could run them at the same time if you want.
* [Local python venv](#local-environment)
* [Shared Hosting](#shared-hosting) (Still Testing)
* [Docker](#docker-environment)
* [AWS Serverless](#aws-serverless) (Still under Development)
* [Digital Ocean](#digital-ocean) (Still under Development)
* [Heroku](#heroku) (Still under Development)
* [React Native](#react-native) (Still under Development)
* [Desktop Native](#desktop-native)

## Local Environment

> To create and develop a local application, we are using [virtualenv](https://pypi.org/project/virtualenv/). A tool for creating isolated virtual python environments.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you can search for "cmd" in your windows search
            * Right-click on the icon, and click on the "Run as administrator" option
                * You may need to navigate to your project when running as administrator `cd <Path To>/my_awesome_project`
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

flask run --port 5000

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you run the command as `sudo` eg: `sudo pip install --upgrade pip`
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

flask run --port 5000

```

## Shared Hosting

> Some shared hosting services offer the ability to run python applications on their servers. I personally have used [A2hosting](http://www.a2hosting.com/refer/171923). Their support has been amazing, and the price to features is one of the best I have come across.

> **Note:** You are not limited to A2 as a shared hosting option. However, this is where I have tested Flask-BDA and have my experience in uploading and running a shared hosting option. If your shared hosting option offers a similar set of features, please feel free to use them.

> For A2, you will need to set up your server to run a python application which may require some configuration for [example](https://www.a2hosting.co.za/kb/developer-corner/python/installing-and-configuring-flask-on-linux-shared-hosting).

> To get your custom application to work:
* You will first need to upload your files (I find this easiest to zip and then upload them to the required location).
* Unzip them on the server and ensure they are in the folder location you require
* Log in to cPanel again to update the python configuration
    * Click the `Setup Python App` again
    * Edit the existing application
    * Change the `Application startup file` to `run_shared_server.py`
    * Restart the server, and your application should now be working as expected.

## Docker Environment

> To create and deploy a containerized application, we are using [Docker](https://www.docker.com/), which helps developers and development teams build and ship apps. In addition, Docker is used for the building and sharing of containerized applications and microservices.

> **Note:** If you are using [Github](https://github.com/) and have docker installed (details on how to install later in the documentation), you will get a new image built every time you `push` or do a `pull_request` on Github, which is set up in the file: `docker-image.yml` however if you want to do this manually, please follow the steps below:

### Windows
* Open a browser and install docker desktop
    * Go to [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
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

> To create and deploy a serverless application, we are using [The Serverless Framework](https://www.serverless.com/), which allows for a zero-friction serverless development, allowing you to easily build apps that auto-scale on low cost, next-gen cloud infrastructure.
> 
> The Serverless framework is an open-source tool that provides an easy YAML + CLI development and deployment to AWS, Azure, Google Cloud, Knative & more.

> **Note:** You may need to adjust the default database strings before del=polying as serverless does not support "SQLite" as the function does not keep state.
> 
> To update the database strings, please refer to [Config]

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

> **Note:** If the package does not install, you may need to run the command as an admin.
> 
> press the  "Windows-Key" type "cmd", "Right-Click" on the word "Command Prompt" and select the option "Run as administrator" and then follow the previous steps again

* Open a browser and install docker desktop:
    * Go to [https://hub.docker.com/editions/community/docker-ce-desktop-windows/](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) to get the installer
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
    * Go to [https://app.serverless.com/](https://app.serverless.com/) to see the deployed application

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

* Open a browser and go to [https://app.serverless.com/](https://app.serverless.com/) to see the deployed application

## Digital Ocean

> **Note:** Still under development

> [Digital Ocean](https://www.digitalocean.com/) is a platform as a service (PaaS). Develop, manage, and scale your applications on DigitalOcean’s complete cloud platform. Digital Ocean provides you with simple, predictable pricing. Confidently build and release with scalable compute products in the cloud, fully managed databases, highly available and scalable storage options, and more. With virtual machines with a healthy amount of memory tuned to host and scale applications and databases Digital Ocean offers simple solutions for complex issues.

> To create and deploy an application to Heroku from the terminal you will need to:
* [Create a droplet](https://docs.digitalocean.com/products/droplets/how-to/create/)
    * Suggested [ubuntu-18-04]
    * Once you see the IP address, you can log in to your Droplet.
        * Make sure you copy/have access to the droplets <ip_address> e.g.: `138.197.67.25`
* [Connect with SSH](https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/)
    * > **NOTE** if you have not connected via SSH you should recieve the `password` via the email that you registered the account, for Digital Ocean, with.
* [Initial server setup](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/<my_awesome_project>/

scp -r <my_awesome_project> root@<ip_address>:/

ssh root@<ip_address>

```
> Where `<Path To>/<my_awesome_project>/` is the path to the project you created
> and where `<ip_address>` is the droplets <ip_address> e.g.: `138.197.67.25`

> **NOTE:** Follow any prompts presended by the ssh such as allowing access from the remote server.

Once you are logged in you should be able to see a terminal with:
```shell
root@<droplet_name>:

cd <Path To>/<my_awesome_project>/

chmod +x setup.sh

bash setup.sh

virtualenv venv

source venv/bin/activate

sudo pip install --upgrade pip
sudo pip install --no-cache-dir -r requirements.txt
sudo pip install uwsgi

sudo ufw allow 5000

export FLASK_APP=app

uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

```
> Where `5000` is the port number  
> and `<droplet_name>` is the name  

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/<my_awesome_project>/

scp -r <my_awesome_project> root@<ip_address>:/

ssh root@<ip_address>

```
> Where `<Path To>/<my_awesome_project>/` is the path to the project you created
> and where `<ip_address>` is the droplets <ip_address> e.g.: `138.197.67.25`

> **NOTE:** Follow any prompts presended by the ssh such as allowing access from the remote server.

Once you are logged in you should be able to see a terminal with:
```shell
root@<droplet_name>:

cd <Path To>/<my_awesome_project>/

chmod +x setup.sh

bash setup.sh

virtualenv venv

source venv/bin/activate

sudo pip install --upgrade pip
sudo pip install --no-cache-dir -r requirements.txt
sudo pip install uwsgi

sudo ufw allow 5000

export FLASK_APP=app

uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

```
> Where `5000` is the port number  
> and `<droplet_name>` is the name



## Heroku

> **Note:** Still under development

> [Heroku](https://www.heroku.com/) is a platform as a service (PaaS). Heroku allows you to start with zero commitment, pay as you go with no lock in. Developers, teams, and businesses of all sizes can use Heroku to deploy, manage, and scale apps. Whether you're building a simple prototype or a business-critical product, Heroku's fully-managed platform gives you a simple path to delivering apps quickly.

> To create and deploy an application to Heroku from the terminal you will need to download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
to verify the installation, you can check the Heroku version from the terminal:
```script
heroku --version

```

> **Note:** Make sure you have changed your database connection, as Heroku does not suggest using SQLite, since the data may be lost on the files. Heroku does offer a free Postgres Database. see their [plans](https://elements.heroku.com/addons/heroku-postgresql) and choose the right plan for you as there are limits on the different plans.

### Windows
* Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) 
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

heroku login

```
* Follow the prompts to log into the Heroku system from the CLI
* Next, create a unique name for your Web app `<my_awesome_project-flask-bda-app>`, where `<my_awesome_project-flask-bda-app>` is the name you gave your project.
* Push your code to Heroku with git

```shell
heroku create my_awesome_project-flask-bda-app
git push heroku master

```
* Finally, web app will be deployed on [http://my_awesome_project-flask-bda-app.herokuapp.com](http://my_awesome_project-flask-bda-app.herokuapp.com) where `<my_awesome_project-flask-bda-app>` is the name you gave your project.

### Linux
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

sudo snap install --classic heroku

heroku login

```
* Follow the prompts to log into the Heroku system from the CLI
* Next, create a unique name for your Web app `<my_awesome_project-flask-bda-app>`, where `<my_awesome_project-flask-bda-app>` is the name you gave your project.
* Push your code to Heroku with git

```shell
heroku create my_awesome_project-flask-bda-app
git push heroku master

```
* Finally, web app will be deployed on [http://my_awesome_project-flask-bda-app.herokuapp.com](http://my_awesome_project-flask-bda-app.herokuapp.com) where `<my_awesome_project-flask-bda-app>` is the name you gave your project.

### Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

brew tap heroku/brew && brew install heroku

heroku login

```
* Follow the prompts to log into the Heroku system from the CLI
* Next, create a unique name for your Web app `<my_awesome_project-flask-bda-app>`, where `<my_awesome_project-flask-bda-app>` is the name you gave your project.
* Push your code to Heroku with git

```shell
heroku create my_awesome_project-flask-bda-app
git push heroku master

```
* Finally, web app will be deployed on [http://my_awesome_project-flask-bda-app.herokuapp.com](http://my_awesome_project-flask-bda-app.herokuapp.com) where `<my_awesome_project-flask-bda-app>` is the name you gave your project.

## React Native

> For native mobile apps, we are using react-native. Specifically, we use [expo](https://expo.io/) as a framework and a platform for universal React applications. It is a set of tools and services built around React Native and native platforms that help you develop, build, deploy, and quickly iterate on iOS, Android, and web apps from the same JavaScript/TypeScript codebase.

> We have pre-sett up push notifications, so you don't have to. This means that it is faster and easier for you to get started and up and running. In addition, we are leveraging the default [expo-notifications](https://github.com/expo/expo/tree/master/packages/expo-notifications) package it allows for a simplified implementation and approach.

> Advantages include faster build and testing workflows/processes, remote testing while developing with Over The Air (OTA) updates with changes visible on saving during development.

> However, there are some disadvantages and [Limitations](https://docs.expo.io/introduction/why-not-expo/) Expo is aware of these and describes them quite well. We suggest reviewing these limitations before using our pre-built method.

> Build one project that runs natively on all your users' devices.

## Install Expo
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

> In the quickstart example, we created a project called `"My Awesome Project"`. However, you may have called the project something else.
> This would have created a folder where the name is all in lower case and stripped out all of the special characters, and replaced spaces with underscores, e.g.: `my_awesome_project`.

> For mobile, we will have automatically created a separate `"_mobile_app"` folder where the prefix of the folder is your project name, e.g. `my_awesome_project_mobile_app`. This is to prevent issues with the `Serverless` configuration `package.json` and allow you not to deploy all the code for a mobile app onto your web server.


#### run a local instance on Public URL with ngrok

> If you are still in development and/or have not chosen a service provider for hosting yet, you could use: [Ngrok](https://ngrok.com/) to create a temporary public development URL that tunnels to your local environment. Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels. This allows you to demo websites on a public URL and test mobile apps connected to your locally running backend without deploying.

* Start the local development server by following the [Local Environment](#local-environment) instructions

* If you have not registered for ngrok before:
    * Open a browser and register for ngrok:
        * Go to: [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
        * Follow the installation instructions and then continue to the next steps
* If you have already registered but do not have it installed:
    * Open a browser and register for ngrok:
        * Go to: [https://dashboard.ngrok.com/get-started/setup](https://dashboard.ngrok.com/get-started/setup)
        * download the correct version for your OS and run the application.
* Once the ngrok terminal is open, create a tunnel from your local server to ngrok
    * create the tunnel to ngrok from the:
        * If you have changed the port number from the default `5000`, then replace the number after `http` to allow the correct tunnel to be created.
    
```shell
ngrok http 5000

```

* This should return a randomly generated URL that you can now use for testing, e.g.:
```shell
ngrok by @inconshreveable
(Ctrl+C to quit) 
Session Status                online
Session Expires               1 hour, 59 minutes
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://573d4ec93267.ngrok.io -> http://localhost:5000
Forwarding                    https://573d4ec93267.ngrok.io -> http://localhost:5000

Connections
ttl     opn     rt1     rt5     p50     p90
0       0       0.00    0.00    0.00    0.00

```

> **Note:** the free version only keeps this server alive for 2 hours, so you may need to follow this process in the future, and if you push this URL to your "Repo", it may not work for the next person.


#### Update the mobile App URL

* Open the Mobile App folder `my_awesome_project_mobile_app`
    * Once open, select the `app.json` file and edit line 2 `"server_base_url": "https://github.com/RyanJulyan/Flask-BDA"` by replacing `https://github.com/RyanJulyan/Flask-BDA` with your own server name.

### Run App
* Install the `expo` App on your own mobile phone by searching for "expo" on the Apple or Google Play Store:
    * `iOS` Go to: [https://apps.apple.com/app/apple-store/id982107779](https://apps.apple.com/app/apple-store/id982107779)
    * `Android` Go to: [https://play.google.com/store/apps/details?id=host.exp.exponent](https://play.google.com/store/apps/details?id=host.exp.exponent)

> Once you have the app installed on your phone, you can start a development server on your local machine.

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

> **Note:** if you wish for people not on your network to be able to scan and test the App remotely, press the `tunnel` tab button above the QR code.

### Deploying to stores
* Open browser and review expo's recommendations to ensure you are ready to deploy:
    * Go to:https://docs.expo.io/distribution/app-stores/
* Open browser and review expo's recommendations on building for the different platforms:
    * Go to:https://docs.expo.io/distribution/building-standalone-apps/

> Part of the recommendations is to ensure that images are optimized. To do this expo has recommended the [expo-optimize package](https://github.com/expo/expo-cli/tree/master/packages/expo-optimize#-welcome-to-expo-optimize) which can assist with optimizing images. In addition, optimizing images can improve your native app TTI (or time-to-interaction), which means less time on splash screens and quicker delivery over poor network connections.

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

> To create and develop a desktop application, we are using [flaskwebgui](https://github.com/ClimenteA/flaskwebgui). A tool for creating and running your flask web application in a chrome wrapper. To distribute the desktop application, we are using [PyInstaller](http://www.pyinstaller.org/). PyInstaller freezes (packages) Python applications into stand-alone executables under Windows, GNU/Linux, Mac OS X, FreeBSD, Solaris and AIX.

> Each deployment needs to be created on the specific platform that you wish to run it. We have created scripts that will allow you to manage these deployments by placing the `build` and `dist` folders into parent folders for the respective platform. These folders will be prefixed with `desktop_` followed by the platform. This is done purely to allow you to manage the distribution and build processes for the specific platforms and not overwrite them when building on different platforms.

> To allow for the export to desktop to work correctly, we require some code changes. By default, Flask-BDA is intended for web and mobile development, and we have implemented a rate-limiter on the site. Unfortunately, you require a server to rate limit, and since you are exporting the system to a desktop application, it is not running a server.
>
> as such, you need to remove all references to the limiter. These can be found at `app/__init__.py`. To do this, open the file in a text editor and comment out the following lines:
```python
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=app.config['DEFAULT_LIMITS']
# )

```

> **Note:** if you added a custom limiter, search for `@limiter.limit`, which would be found in your controllers. You will need to comment out all of those references and the import references, e.g.: `from app import limiter`

> This will allow you to export the application as a desktop executable file without errors.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you can search for "cmd" in your windows search
            * Right-click on the icon, and click on the "Run as administrator" option
                * You may need to navigate to your project when running as administrator `cd <Path To>/my_awesome_project`
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
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you run the command as `sudo` eg: `sudo pip install --upgrade pip`
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
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you run the command as `sudo` eg: `sudo pip install --upgrade pip`
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

> By default, this application will be served on port `7000`. However, you can edit the port in the `run_desktop.py` file if that conflicts with any existing applications.

# Installing Additional Python Packages

> If you include additional python packages in your project, don't forget to run `pip freeze` from your terminal to ensure you get the correct packages for your deployments

```shell
pip freeze > requirements.txt

```

> **Note:** It is suggested that you install and freeze Additional Python Packages from a virtual environment rather than globally. This keeps your `requirements.txt` small and limited to the packages you are using in your specific project.

# OpenAPI/Swagger API

> Flask BDA uses [SwaggerUI](https://swagger.io/tools/swagger-ui/) by default to assist and present the API to a user/client.

> SwaggerUI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. Instead, it’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with visual documentation making it easy for back-end implementation and client-side consumption.

To Access the SwaggerUI:
* Go to your browser and insert the URL `<base_URL>/api/docs` to access the SwaggerUI API, e.g.: [`http://localhost:5000/api/docs`](http://localhost:5000/api/docs)

# Import API to Postman

> Many developers will prefer [Postman](https://www.postman.com/) over [SwaggerUI](https://swagger.io/tools/swagger-ui/) to test and integrate APIs with their code. We have assisted by providing a direct collection export for Postman.

> To import the collection on Postman:
* Ensure you have downloaded and installed [Postman](https://www.postman.com/downloads/)
* Once installed, click on 'file' (on the top left of the application menu bar)
* Choose `Import...` (CTRL+O)
* Select `Link` from the Tabs
* Insert the URL `<base_URL>/api/postman` eg: [`http://localhost:5000/api/postman`](http://localhost:5000/api/postman)
* Press `Continue`
* This will show you the name of the API as defined in the API config
* Review and click `Import`

> This will import a postman collection which will become available on the left-hand side as a folder (with subfolders from each of the endpoints you created).

> You can [generate code](https://learning.postman.com/docs/sending-requests/generate-code-snippets/) for many different [lanuages and frameworks](https://learning.postman.com/docs/sending-requests/generate-code-snippets/#supported-languagesframeworks) using Postman. These Languages include but are not limited to:
* C
* C#
* Go
* Java
* Javascript
* Node
* PHP
* Python
* Powershell
* Ruby
* Swift

> Allowing you to integrate your newly created API with existing projects


# External API Requests

> Sometimes, you need to make external requests (e.g. to an external API). You could approach this using [Ajax Requests](#ajax-requests), but sometimes you need to make these requests from the server-side, for example, if you want to update currency conversions automatically. When you want to access external APIs through the server, you do not want to rely on a user actively being on the webpage to send the command. Instead, you want the server to be able to activate this comment. To achieve this, we use the [requests module](https://www.w3schools.com/python/module_requests.asp).

* The structure of a request is:
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

### Post JSON Request Method
```python
import requests
import json

data = {"Name":"Example"}
headers = {"Authorization": "Bearer <token>"}

x = requests.post('https://w3schools.com/python/demopage.php', json = data, headers = headers)
print(x.status_code)
print(x.text)

# use this to load JSON returned as a python dictionary
return_data = json.loads(x.text)

```

### Put Request Method
```python
import requests

data = {"Name":"Example"}
headers = {"Authorization": "Bearer <token>"}

x = requests.put('https://w3schools.com/python/demopage.php', data = data, headers = headers)
print(x.status_code)
print(x.text)

```

### Put JSON Request Method
```python
import requests
import json

data = {"Name":"Example"}
headers = {"Authorization": "Bearer <token>"}

x = requests.put('https://w3schools.com/python/demopage.php', json = data, headers = headers)
print(x.status_code)
print(x.text)

# use this to load JSON returned as a python dictionary
return_data = json.loads(x.text)

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

> htmx is a dependency-free library that allows you to access AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly in HTML, using attributes so that you can build modern user interfaces with the simplicity and power of hypertext. For details on how to use htmx, please refer to the [docs](https://htmx.org/docs/) and for a full reference on the functionality, please refer to [https://htmx.org/reference/](https://htmx.org/reference/)

You can use htmx to implement many common UX patterns, such as Active Search:
```html
<input type="text" name="q" 
    hx-get="/trigger_delay" 
    hx-trigger="keyup changed delay:500ms" 
    hx-target="#search-results" 
    placeholder="Search..."/>

<div id="search-results"></div>
```
This input named q will issue a request to `/trigger_delay` 500 milliseconds after a key-up event if the input has been changed and inserts the results into the div with the id search-results.

# Testing

> Testing is a vital part of ensuring a project runs successfully

There are 3 aspects of testing provided in Flask BDA:
* CI/CD through [Github actions workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions) which is already set up to implement but can also be used independently from GitHub:
    * Python [flake8](https://flake8.pycqa.org/en/latest/) code [linting](#linting).
        * It displays the warnings in a per-file, merged output. Flake8 is a wrapper around these tools:
            * PyFlakes
            * pycodestyle
            * Ned Batchelder’s McCabe script
    * Python [unittest](https://docs.python.org/3/library/unittest.html) originally inspired by JUnit and has a similar flavour as major [unit testing](#unit-testing) frameworks in other languages.

# Python flake8

> **Note:** To manually run Python `unittest`, ensure that you have installed the [local environements](#local-environment)

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

> **Note:** To manually run Python `unittest`, ensure that you have installed the [local environements](#local-environment)

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
* Starter flask project, which builds a project folder structure with
    * Flask microframework
        * Quick and easy
        * Ability to scale up
        * One of the most popular Python web application frameworks.
        * Doesn't enforce any dependencies or project layout.
    * Progressive Web App (PWA) to make it more friendly towards desktop and allow native installs from the web, cache for offline support, page sharing and push notifications, etc.
    * Responsive layouts
    * Mobile-specific views through [Flask-Mobility](https://github.com/rehandalal/flask-mobility)
        * Responsive bottom menu for tablet and mobile devices
            * Centered for tablet at under `992px`
            * Centered for mobile at under `500px`
            * Badges for notifications are included to allow for driving user behaviour
        * Controllers use the `@mobile_template` decorator, allowing template views to be tailored for a better mobile experience if needed.
        * Mobile view identification meaning specific mobile logic, can be added with `{% if request.MOBILE %}True{% else %}False{% endif %}`
    * SEO ready page index template file
    * Isolated module code and templates
    * Configuration file `config.py` for quick access and management of the environment and environment variables and default SEO
    * Debugging built-in and accessible through the Configuration file `config.py`
    * A Landing page with a call to action and features
    * A 403 page which all forbidden pages go to
    * A 404 page which all unknown pages go to
    * .gitignore files with defaults
    * [Testing](#testing) with Python [flake8](https://flake8.pycqa.org/en/latest/) Linting and Test cases Python [unittest](https://docs.python.org/3/library/unittest.html)
    * CI/CD through [Github actions workflow](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions)
    * Can run in any cloud or your data centre.
        * Server entry point file for shared hosting from "run.py" 
        * [Local virtual Python environment](#local-environment)
        * [Docker virual environment config](#docker-environment)
            * Removes tons of headaches when setting up your dev environment
            * Prevents issues such as "well, it worked on my machine!"
        * [AWS Serverless yml config](#aws-serverless)
    * Great UI by default with [AdminLTE](https://adminlte.io/) specifically [v3](https://adminlte.io/themes/v3/)
        * Highly customizable and flexible
        * Pre-setup via CDN
        * Versatile
        * Widely used and easy to pick up as it is based on [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/)


* Create custom [module](#modules) files and folders that fit into the flask project structure from the `create_module.py` file with prompts to create the following:
    * Model
        * Dynamically create a table data model 
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
    * URL's (prefixed by the module name and replace 'xyz' with the module name in the below details)
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
            * POST URL ../api/xyz/bulk [multiple elements] `post`
            * PUT URL ../api/xyz/bulk [multiple elements] `update`
            * GET URL ../api/xyz/aggregate [single return, of multiple elements aggregated] `get`
    * Views for:
        * Public
            * `public_list.html` (list elements)
        * Admin
            * `index.html` (list elements)
            * `create.html` (single element form)
            * `show.html` (single element)
            * `edit.html` (single element form)
        * API
            * `api/docs` (URL)

## Project Structure
```
└── `project_name`
       ├── .github
       │    └── workflows
       │          ├── docker-image.yml
       │          └── run_tests.yml
       ├── app
       │    ├── generated_config
       │    │     ├── model_editor
       │    │     └── models
       │    │           ├── hierarchies
       │    │           │   └── models.json
       │    │           └── organisations
       │    │               └── models.json
       │    ├── mod_audit
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     └── models.py
       │    ├── mod_users
       │    │     ├── templates
       │    │     │     ├── mobile
       │    │     │     │    └── auth
       │    │     │     │         ├── admin
       │    │     │     │         │    ├── create.html
       │    │     │     │         │    ├── edit.html
       │    │     │     │         │    ├── index.html
       │    │     │     │         │    └── show.html
       │    │     │     │         └── public
       │    │     │     │              └── public_list.html
       │    │     │     ├── email
       │    │     │     │    ├── activate.html
       │    │     │     │    └── reset.html
       │    │     │     └── users
       │    │     │          ├── admin
       │    │     │          │    ├── create.html
       │    │     │          │    ├── edit.html
       │    │     │          │    ├── index.html
       │    │     │          │    └── show.html
       │    │     │          └── public
       │    │     │               └── public_list.html
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     ├── forms.py
       │    │     └── models.py
       │    ├── mod_email
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     └── models.py
       │    ├── mod_file_upload
       │    │     ├── templates
       │    │     │    └── file_upload
       │    │     │         └── upload.html
       │    │     ├── __init__.py
       │    │     ├── controllers.py
       │    │     ├── forms.py
       │    │     └── models.py
       │    ├── static
       │    │     ├── css
       │    │     ├── images
       │    │     ├── js
       │    │     ├── manifest.json
       │    │     └── sw.js
       │    ├── templates
       │    │     ├── admin
       │    │     │     └── index.html
       │    │     ├── email
       │    │     │     └── auth
       │    │     │         ├── activate.html
       │    │     │         └── reset.html
       │    │     ├── mobile
       │    │     ├── public
       │    │     │     └── index.html
       │    │     ├── 403.html
       │    │     ├── 404.html
       │    │     └── index.html
       │    └── __init__.py
       ├── create_module_template
       │    ├── generated_config
       │    │     └── models
       │    │          └── xyz
       │    │               └── models.json
       │    └── mod_xyz
       │          ├── templates
       │          │     ├── mobile
       │          │     │    └── xyz
       │          │     │         ├── admin
       │          │     │         │    ├── create.html
       │          │     │         │    ├── edit.html
       │          │     │         │    ├── index.html
       │          │     │         │    └── show.html
       │          │     │         └── public
       │          │     │              └── public_list.html
       │          │     └── xyz
       │          │          ├── admin
       │          │          │    ├── create.html
       │          │          │    ├── edit.html
       │          │          │    ├── index.html
       │          │          │    └── show.html
       │          │          └── public
       │          │               └── public_list.html
       │          ├── api_controllers.py
       │          ├── controllers.py
       │          ├── forms.py
       │          └── models.py
       ├── databases
       │    └── sqlite
       │          ├── core.db
       │          └── default.db
       ├── .dockerignore
       ├── .gitignore
       ├── config.py
       ├── create_all_models_json.py
       ├── create_desktop_installer_lunix.py
       ├── create_desktop_installer_mac.py
       ├── create_desktop_installer_windows.py
       ├── create_module.py
       ├── create_module_json.py
       ├── Dockerfile
       ├── FLASK-BDA LICENSE
       ├── LICENSE
       ├── package.json
       ├── package-lock.json
       ├── Procfile
       ├── README.md
       ├── requirements.txt
       ├── run.py
       ├── run_desktop.py
       ├── run_shared_server.py
       └── serverless.yml
```

# Glossary
## Modules
### Introduction
> A module is a part of a program. Programs are composed of one or more independently developed modules that, when combined, create the program. 
> 
> A module is a self-contained component, making it easier to manage as the program grows.
> 
> Modules in Flask-BDA help you create: a Data Model, Routes, and associated functions for controlling the logic and Views

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
> A low-code development platform provides a development environment to create application software through programmatic or graphical user interfaces and configurations instead of traditional hand-coded computer programming.

________________________________________

# How can I help?

We would be delighted if you contributed to the project in one or all of these ways:

* Talking about Emmett with friends and on the web
* Adding issues and features requests here on GitHub
* Participating in discussions about new features and issues here on GitHub
* Improving the documentation
* Forking the project and writing beautiful code

# License

## Python 3

View license information for Python 3. (https://docs.python.org/3.8/license.html) and other legal agreements (https://www.python.org/about/legal/)

________________________________________

## Docker

View license information for Docker. (https://www.docker.com/legal/components-licenses) and other legal agreements (https://www.docker.com/legal)

As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc., from the base distribution, along with any direct or indirect dependencies of the primary software being contained).

Some additional license information that could be auto-detected might be found in the repo-info repository's python/ directory.

As for any pre-built image usage, the image user's responsibility is to ensure that any use of this image complies with any relevant licenses for all software contained within.

________________________________________

## Serverless Framework

View license information for Serverless Framework and other legal agreements (https://app.serverless.com/legal/terms).

It is the user's responsibility to ensure that adhere to the Acceptable Use Policy (https://app.serverless.com/legal/aup)

________________________________________

## Expo Framework

View license information for the Expo Framework and other legal agreements (https://github.com/expo/expo/blob/master/LICENSE).

________________________________________

## The Flask-BDA License

Flask-BDA is created and distributed under the developer-friendly Flask-BDA License. The Flask-BDA License is derived from the popular Apache 2.0 license.

The Flask-BDA License is the legal requirement for you or your company to use and distribute Flask-BDA and derivative works such as the applications you make with it. Your application or project can have a different license, but it still needs to comply with the original one.

### The license grants you the following permissions:
* You are free to commercialize any software created using original or modified (derivative) versions of Flask-BDA
* You are free to commercialize any plugin, extension, or tool created for use with Flask-BDA
* You are free to modify Flask-BDA, and you are not required to share the changes
* You are free to distribute original or modified (derivative) versions of Flask-BDA
* You are given a license to any patent that covers Flask-BDA

### The license prevents you from doing the following:
* You can not commercialize original or modified (derivative) versions of the Flask-BDA editor, creator and/or engine
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
