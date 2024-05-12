# Common Services

<br/>

## Table Of Contents:

#### Installation Process
1. [Repository Goal](#repository-goal)
2. [Quick Start](#quick-start)
3. [Installing Dependencies](#installing-dependencies)
4. [Running Docker](#running-docker)
5. [Running the Local Django Server](#running-the-local-django-server)
6. [Updating Requirements with New Dependencies](#updating-requirementstxt-with-new-dependencies)
7. [Steps to Set Up the MySQL Database for User Database](#steps-to-set-up-the-mysql-database-for-user-database)
#### Django Cheat Sheet
1. [How to make an application](#how-to-make-an-application)
2. [How to add models to an application](#how-to-add-models-to-an-application)
3. [Checking the MySQL Database](#checking-the-mysql-database)

## Repository Goal

This repository will contain the Common Services for both supply and demand cloud. The goal is to be able to add this repo to any project and have a functioning login and sign up system.

<br/>

## Quick Start

If you want to quickly run the server and install dependencies you can run this script:

1. Open Terminal > New Terminal
2. Change Directory to `common-services-repo`

```shell
cd ./common-services-repo
```

<br/>

3. Run this in the terminal

```shell
./start_server.sh
```

<br/>

4. If you get an error about `config` you will need to get the file from the team on Slack

> Note: If you receive an error try troubleshooting by following the steps in this readme file.

<br/>

## Installing Dependencies

1. Inside of `common-services-repo` create a virtual environment called `virtual-env`. This will help you install all the dependencies you need.

```shell
python3 -m venv virtual-env
```

<br/>

2. Inside of `common-services-repo` start the virtual environment with this command. To stop the virtual command simply type `deactivate`

```shell
source virtual-env/bin/activate
```

<br/>

3. Inside of `common-services-repo` install the dependencies you need with this command

```shell
pip install -r requirements.txt
```

<br/>

## Running Docker

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References

* [Docker's Python guide](https://docs.docker.com/language/python/)

## Running the Local Django Server

Inside of `common-services-repo` run this. It will start up the Django Server

```shell
python3 manage.py runserver
```

<br/>

## Updating `requirements.txt` with new dependencies

1. Run you virtual environment again

```shell
source virtual-env/bin/activate
```

<br/>

2. Saves new requirements into the `requirements.txt`

```shell
pip freeze > requirements.txt
```

<br/>

## Steps to set up the MySQL database for user database

Our MySQL database will not be included with our version control. Instead, we will have a MySQL database server running on the Demand cloud. For local testing purposes, we will recreate the MySQL database so that it can still interact with our code. This just means remaking the database with the same username and password. You should only need to do this once.

### Linux Enviornment

1. Go to your `common-services-repo` location.
2. Run the following in the terminal if you’re installing on Linux/Mac (if you’re on Windows try these steps):

```shell
sudo apt update
sudo apt upgrade
sudo apt install mysql-server
```

<br/>

3. Run the following to verify server is running:

```shell
sudo systemctl start mysql
sudo systemctl enable mysql
sudo systemctl status mysql
```

<br/>

4. Run the following to install necessary packages for Django:

```shell
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev
sudo apt update
pip install mysqlclient
```

<br/>

5. Run the following to enter and set up mysql

```shell
sudo mysql
sudo mysql_secure_installation
```

<br/>

6. Run the following to install the necessary package for the mysqlclient and install mysqlclient for the Django server.

```shell
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev
sudo apt update
pip install mysqlclient
```

<br/>

7. Run the following to enter mysql and create the user database:

```shell
sudo mysql
>>> CREATE DATABASE userdb;
>>> CREATE USER 'loginservice_user'@'localhost' IDENTIFIED BY 'cabinetPortraitFaithSwitch';
>>> GRANT ALL PRIVILEGES ON `userdb` . * TO 'loginservice_user'@'localhost';
>>> FLUSH PRIVILEGES;
```

8. To run unit tests on the backend. Make sure you are still logged into root

```mysql
>>> GRANT ALL PRIVILEGES ON `test_userdb`.* TO 'loginservice_user'@'localhost';
>>> FLUSH PRIVILEGES;
```

> NOTE: for GRANT…. userdb is surrounded by ` characters and not ‘.

9. Make sure you migrate your models so that the Database gets updated with the correct tables

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### MacOS Environment

1. Update Homebrew the Package Manager

```shell
brew update
brew upgrade
```

2. Install MySQL Server

```shell
brew install mysql
```

3. Start MySQL Service

```shell
brew services start mysql
```

4. Check MySQL Service Status

```shell
brew services list
```

5. Install Necessary Packages for Django

> The equivalent packages to `pkg-config` and `libmysqlclient-dev` are installed as dependencies with MySQL when using Homebrew, so you don’t need to install them separately. However, you can install `pkg-config` if it’s not already installed by other formulas:

```shell
brew install pkg-config
```

6. Install mysqlclient for Django

> You can use `pip` to install `mysqlclient`. It’s recommended to use a virtual environment for Python projects, but for a global install, just run:

```shell
pip install mysqlclient
```

7. Secure MySQL Installation

> Run the `mysql_secure_installation` command, which will guide you through securing your MySQL installation, including setting the root password, removing anonymous users, disallowing root login remotely, and more:

```shell
mysql_secure_installation
```

8. Enter MySQL Shell

```shell
mysql -u root -p
>>> CREATE DATABASE userdb;
>>> CREATE USER 'loginservice_user'@'localhost' IDENTIFIED BY 'cabinetPortraitFaithSwitch';
>>> GRANT ALL PRIVILEGES ON `userdb` . * TO 'loginservice_user'@'localhost';
>>> FLUSH PRIVILEGES;
```

9. To run unit tests on the backend. Make sure you are still logged into root

```mysql
>>> GRANT ALL PRIVILEGES ON `test_userdb`.* TO 'loginservice_user'@'localhost';
>>> FLUSH PRIVILEGES;
```

10. Make sure you migrate your models so that the Database gets updated with the correct tables

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

<br/>
<br/>
<br/>

# Django Cheat Sheet

<br/>

## How to Make an Application

<br/>

1. Go to the root directory of the Django project.
2. Run the following command:

```shell
python3 manage.py startapp <app_name>
```

> Replace <app_name> with the name of the plug-in

<br/>

3. Register the new app in the `INSTALLED_APPS` setting in the `/myproject/settings.py` file.

```py3
#/myproject/settings.py
...
INSTALLED_APPS = [
	# other apps ...
	‘myapp’,
]
```

<br/>

4. Create a URL path to the application by configuring the /myproject/urls.py file.

```python
#/myproject/urls.py
...
urlpatterns = [
	# other paths ...
	path(‘<app_name>/’, include(‘<app_name>.urls’)),
]
```

<br/>

5. Create a urls.py file within the <app_name> folder and add the following:
   You will add new paths for each view you create for this function.
   This is how we will create API endpoints.

```python
#/myproject/<app_name>/urls.py
from django.urls import path
from . import views

urlpatterns = [
]
```

<br/>

## How to Add Models to an Application

1. Go to the models.py file within the application folder.
   <br/>
2. Write a Class with fields.
   <br/>
3. Perform the following commands in the project folder.

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

<br/>

## Checking the MySQL Database

If you have the correct tables set up follow these steps:

1. Open MySQL then enter the password for the user loginservice_user

```shell
mysql -u loginservice_user -p 
```

2. Select the `userdb` database which will have the user login information

```shell
USE userdb;
```

3. Display everything from the `login_service_baseuser` table

```shell
SELECT * FROM login_service_baseuser;
```

4. The output should look something like this:

```txt
+----+----------------------------+-----------------+----------+----------------------------+----------------------------+-----------+
| id | password                   | email           | username | date_joined                | last_login                 | is_active |
+----+----------------------------+-----------------+----------+----------------------------+----------------------------+-----------+
|  1 | pbkdf2_sha256$600000$C9... | dwadwadw@dwadwa | dwadwa   | 2024-03-02 01:46:21.547857 | 2024-03-02 01:46:21.547877 |         1 |
+----+----------------------------+-----------------+----------+----------------------------+----------------------------+-----------+
```
