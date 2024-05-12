# Map Services

<br/>

## Table Of Contents:

#### Installation Process
1. [Repository Goal](#repository-goal)
2. [Quick Start](#quick-start)
3. [Installing Dependencies](#installing-dependencies)
4. [Docker Documentation](#docker-documentation)
5. [Running the Local Django Server](#running-the-local-django-server)

## Repository Goal
This repository will contain a repository to organize all the calls to Mapbox. The reason we are doing this is to provide extensibility and a separation of concerns. See the [mapbox webiste](https://account.mapbox.com/) for more information and documentation.

<br/>

## Quick Start
If you want to quickly run the server and install dependencies you can run this script:
1. Open Terminal > New Terminal

2. Change Directory to `map-services-repo`
```shell
cd ./map-services-repo
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
1. Inside of `map-services-repo` create a virtual environment called `virtual-env`. This will help you install all the dependencies you need.
```shell
python3 -m venv virtual-env
```
<br/>

2. Inside of `map-services-repo` start the virtual environment with this command. To stop the virtual command simply type `deactivate`
```shell
source virtual-env/bin/activate
```
<br/>

3. Inside of `map-services-repo` install the dependencies you need with this command
```shell
pip install -r requirements.txt
```

<br/>

## Docker Documentation
### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:10000.

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
Inside of `map-services-repo` run this. It will start up the Django Server
```shell
python3 manage.py runserver
```
<br/>

## Updating `requirements.txt` with new dependencies
1. Run you virtual environment again
```shell
source map-services-repo/bin/activate
```
<br/>

2. Saves new requirements into the `requirements.txt`
```shell
pip freeze > requirements.txt
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