# Supply Frontend
<br/>

#### Installation Process
1. [Repository Goal](#repository-goal)
2. [Quick Start](#quick-start)
3. [Installing Node/NPM](#installing-nodenpm)
4. [Installing Dependencies](#installing-dependencies)
5. [Running the Local React Server](#running-the-local-react-server)
6. [Docker Documentation](#docker-documentation)

## Repository Goal
This repository will contain the Supply Cloud Fleet Manager Dashboard, where the fleet manager can add vehicles, remove vehicles, and monitor different aspects of the Wego website. This will contain more data driven graphics and provide the fleet manager with an understanding of what is happening in the 

<br/>

## Quick Start
If you want to quickly run the server and install dependencies follow these steps:
1. Open Terminal > New Terminal

2. Change Directory to `supply-front-end-repo`
```shell
cd ./supply-front-end-repo
```

3. Run this in the terminal
```shell
./start_server
```
> Note: If you receive an error try troubleshooting by following the steps in this readme file.

<br/>

## Installing Node/NPM
Instructions taken from [nvm website](https://github.com/nvm-sh/nvm) and from ChatGPT

1. First install/update nvm by running this:
```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```
> You may have to restart your terminal after this step

2. Install version 20.11.1. This is the current LTS (Long Term Support) version. You can check [here](https://nodejs.org/en)
```shell
nvm install 20.11.1
```

3. Switch to version 20.11.1
```shell
nvm use 20.11.1
```

4. Check that you are using the LTS version
```shell
node -v
```
### Optional
5. List all the installed versions of Node.js
```shell
nvm list
```

6. Remove any extra versions. All this does is clear up disk space
```shell
nvm uninstall 21.5.0
```
> replace 21.5.0 with any version you want to replace

<br/>

## Installing Dependencies
Inside of  `supply-front-end-repo` run this command. It will install the contents of  `package-lock.json` and `package.json` which are all the dependencies you need.
```shell
npm install
```
> NOTE: If you install dependencies they will automatically be recorded in `package-lock.json` and `package.json` so you do not have to worry about telling others to install the same dependencies.

<br/>

## Running the Local React Server
Inside of  `supply-front-end-repo` run this command. It will run the local server where you can view your REACT code.
```shell
npm run dev
```

## Docker Documentation
### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:3000.

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
* [Docker's Node.js guide](https://docs.docker.com/language/nodejs/)