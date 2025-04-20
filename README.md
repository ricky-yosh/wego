# WeGo TAAS Solution

### Contributors

- Andrew Martinez
- Richard Yoshioka
- Alek Marttala
- Anuskha Siwakoti
- Anghelina Opinca
- Jason Castillon
- Tony Reyes

## Background

Finished project for COSC-3339 Software Engineering at St. Edward's Universtiy.
Originally worked on in BitBucket but transferred into GitHub for sharing purpsoes.

## Project

WeGo Service seeks to provide scalable transportation as a service (TaaS) solutions. This is our first public release and our first alpha. We are neither feature complete nor stable but the core functionality is implemented. 

## View the Demo!

https://youtu.be/pfdZyTuQRrk

## Features

### Demand Front End
- Built a front page
- Created rest API interactions for Common Services and Demand Back End servers
- Implemented functioning front end for Construction Wizard, an example product created using WeGo Service tools
### Demand Back End
- Built an extensible plugin framework to quickly set up new tables in the database for Order and Item related only to that plugin.
- Created backend support for two plugins: Construction Wizard and Lifetime Drones
- Created an efficient address handling and storing system.
- Created a customer object to store preferences.
### Supply Front End
- Created an interactive dashboard to manage a fleet of vehicles
### Supply Back End
- Created a Trip object which keeps track of orders requesting a vehicle to make a pickup/delivery.
- Created a Vehicle object which contains live information reported by vehicles as well as information queried by the vehicle, such as if it has a route it needs to go through.
- Created a trip queuing system for unassigned orders to await being assigned a vehicle.
### Map Services
- Contains Rest API calls to MapBox.
- Call to convert a string address to longitude and latitude coordinates.
- Call to generate a route between coordinates and two string addresses.
### Common Services
- Created a BaseUser object which contains a username and a password and is used for authentication purposes.
- Passwords are hashed using Django’s built-in hash function.
### Vehicle Simulator (VSIM)
- Created a python program to simulate multiple vehicles, utilizing multi-threading, to interact with the API endpoints on the Supply cloud.
