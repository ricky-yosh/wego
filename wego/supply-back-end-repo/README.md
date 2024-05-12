# Supply Backend

<br/>
## Table Of Contents:

#### Installation Process
1. [Repository Goal](#repository-goal)
2. [Quick Start](#quick-start)
3. [Installing Dependencies](#installing-dependencies)
4. [Docker Documentation](#docker-documentation)
5. [Running the Local Django Server](#running-the-local-django-server)
6. [Steps to setup the mysql database for user database](#steps-to-set-up-the-mysql-database-for-user-database)
#### Django Cheat Sheet
1. [How to make an application](#how-to-make-an-application)
2. [How to add models to an application](#how-to-add-models-to-an-application)
3. [Checking the MySQL Database](#checking-the-mysql-database)

## Quick Start
If you want to quickly run the server and install dependencies you can run this script:
1. Open Terminal > New Terminal

2. Change Directory to `supply-back-end-repo`
```shell
cd ./supply-back-end-repo
```
<br/>

3. Run this in the terminal
```shell
./start_server
```
<br/>

4. If you get an error about `config` you will need to get the file from the team on Slack

> Note: If you receive an error try troubleshooting by following the steps in this readme file.

<br/>

## Installing Dependencies
1. Inside of `supply-back-end-repo` create a virtual environment called `virtual-env`. This will help you install all the dependencies you need.
```shell
python3 -m venv virtual-env
```
<br/>

2. Inside of `supply-back-end-repo` start the virtual environment with this command. To stop the virtual command simply type `deactivate`
```shell
source virtual-env/bin/activate
```
<br/>

3. Inside of `supply-back-end-repo` install the dependencies you need with this command
```shell
pip install -r requirements.txt
```

<br/>

## Repository Goal
This repository will contain the backend of the Supply Cloud which will contain the Fleet Manager. It will contain Fleet, which manages all of the registered WeGo vehicles. Dispatcher will also be here, which manages the order and finds available vehicles to combine them and make the trip.

<br/>

## Docker Documentation
### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:9000.

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

<br/>

## Running the Local Django Server
Inside of `supply-back-end-repo` run this. It will start up the Django Server
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

## Steps to set up the Mongo database for fleet database

Our Mongo database will not be included with our version control. Instead, we will have a Mongo database server running on the Supply cloud. For local testing purposes, we will recreate the Mongo database so that it can still interact with our code. This just means remaking the database with the same username and password. You should only need to do this once.

### Linux Enviornment
> See the [official MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) site for how to install on Ubuntu if these steps do not work.

1. Go to your `supply-back-end-repo` location.

2. Update Advanced Package Tool
```shell
sudo apt update
sudo apt upgrade
```
<br/>

3. Open up the virtual environment:
```shell
source virtual-env/bin/activate
```
<br/>

4. Install the dependencies:
```shell
pip install -r requirements.txt
```
<br/>

5. From a terminal, install `gnupg` and `curl` if they are not already available:
```shell
sudo apt-get install gnupg curl
```
<br/>

6. To import the MongoDB public GPG key, run the following command:
```shell
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```
<br/>

7. Create the /etc/apt/sources.list.d/mongodb-org-7.0.list file for Ubuntu 22.04 (Jammy):
```shell
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```
<br/>

8. Reload local package database
```shell
sudo apt-get update
```
<br/>

9. Install the MongoDB packages
```shell
sudo apt-get install -y mongodb-org
```
<br/>

10. Start MongoDB
```shell
sudo systemctl start mongod
```
<br/>

11. Reload daemons
```shell
sudo systemctl daemon-reload
```
<br/>

12. Verify that MongoDB has started successfully.
```shell
sudo systemctl status mongod
```
<br/>

13. Ensure the MongoDB will start following a system reboot
```shell
sudo systemctl enable mongod
```
<br/>

14. Restart MongoDB.
```shell
sudo systemctl restart mongod
```
<br/>

15. Enter MongoDB Shell
```shell
mongosh
```
<br/>

16. Enter the admin database
```shell
use admin
```
<br/>

17. Create the user that the django application will use to update the database of vehicles
```shell
db.createUser({
  user: "fleet_admin",
  pwd: "**********",
  roles: [
    { role: "dbAdmin", db: "fleetdb" }
  ]
})
```
> You will need to ask in the Slack what the password is. This is to make efforts to improve security in the application.

<br/>

18. Make sure you migrate your models so that the database gets updated with the correct tables
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```
<br/>

19. If you run into this error:
```
raise ImproperlyConfigured(
django.core.exceptions.ImproperlyConfigured: 'djongo' isn't an available database backend or couldn't be imported. Check the above exception. To u
se one of the built-in backends, use 'django.db.backends.XXX', where XXX is one of:
    'mysql', 'oracle', 'postgresql', 'sqlite3
```
Run this in the terminal (make sure that you are in the virtual environment `source virtual-env/bin/activate`)
```shell
pip uninstall pymongo==3.12.3
pip install pymongo==3.12.3
```

```shell
pip install sqlparse==0.2.4
```

```shell
pip install pytz
```
<br/>

20. If you run into this error:
```
raise NotImplementedError( NotImplementedError: Database objects do not implement truth value testing or bool(). Please compare with None instead: database is not None
```
Run this in the terminal (make sure that you are in the virtual environment `source virtual-env/bin/activate`)
```shell
pip uninstall pymongo==3.12.3
pip install pymongo==3.12.3
```
<br/>
<br/>

### MacOS Environment
1. Go to your `supply-back-end-repo` location.

2. Update Homebrew the Package Manager
```shell
brew update
brew upgrade
```
<br/>

3. Open up the virtual environment:
```shell
source virtual-env/bin/activate
```
<br/>

4. Install the dependencies:
```shell
pip install -r requirements.txt
```
<br/>

5. Install Djongo (a connector that allows users to use MongoDB as the backend)
```shell
pip install djongo
```
<br/>

6. Install mongodb and the community version
```shell
brew tap mongodb/brew
brew install mongodb-community
```
<br/>

7. Start the community version of MongoDB
```shell
brew services start mongodb-community
```
<br/>

8. Install the shell for mongo
```shell
brew install mongosh
```
<br/>

9. Check mongodb-community status
```shell
brew services list
```
<br/>

10. Enter MongoDB Shell
```shell
mongosh
```
<br/>

11. Enter the admin database
```shell
use admin
```
<br/>

12. Create the user that the django application will use to update the database of vehicles
```shell
db.createUser({
  user: "fleet_admin",
  pwd: "**********",
  roles: [
    { role: "dbAdmin", db: "fleetdb" }
  ]
})
```
> You will need to ask in the Slack what the password is. This is to make efforts to improve security in the application.

<br/>

13. Make sure you migrate your models so that the database gets updated with the correct tables
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```
<br/>

14. If you run into this error:
```
raise NotImplementedError( NotImplementedError: Database objects do not implement truth value testing or bool(). Please compare with None instead: database is not None
```
Run this in the terminal (make sure that you are in the virtual environment `source virtual-env/bin/activate`)
```shell
pip uninstall pymongo==3.12.3
pip install pymongo==3.12.3
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

## Checking the Mongo Database
MongoDB is a NoSQL Database so there are no traditional tables. Instead there are **Collections** and **Documents**.
1. **Collections** are similar to tables. They contain sets of documents.

2. **Documents** are similar to rows in a table. Each document is BSON (Binary JSON)

### View a Collection
1. View all the databases:
```shell
show dbs
```

2. Select the database. In our case it will be `fleetdb`.
```shell
use fleetdb
```
<br/>

3. View collections
```shell
show collections
```
<br/>

4. Show the specified collection that you want to see:
```shell
db.<collection_name>.find()
```