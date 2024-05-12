**Vehicle Simulator (VSIM)**

**Overview**
The Vehicle Simulator (VSIM) is a Python-based simulation system designed to emulate the behavior
and movement of vehicles within a simulated environment. This project allows for the 
dynamic simulation of vehicle movements, interactions, and status changes, providing a 
foundational tool for understanding vehicle dynamics and control systems.

**Components**
The project consists of several key Python files:
* VSIM.py: The main entry point for the vehicle simulation, handling user inputs, simulation initialization, and control flow.
* Car.py: Defines the Car class, a specific type of vehicle with attributes and behaviors relevant to cars.
* Vehicle.py: Contains the Vehicle class, serving as the base class for different types of vehicles within the simulation.
* VehicleStatus.py: Provides the VehicleStatus class to manage and update the status of each vehicle during the simulation.
* VSIM_Tester.py: A testing script to validate the functionality and performance of the vehicle simulator.

**Features**
* Simulate multiple vehicles concurrently within the environment.
* Dynamically control vehicle movements and status.
* Extendable framework for adding different types of vehicles and behaviors.
* Interactive user inputs to control simulation parameters and actions.
* Get a resume of the fleet.
* API calls to the supply cloud, to update car status. 

**Requirements**
Python 3.9.6

**Usage**
To start the simulation, run the VSIM.py script from the command line:

Copy code:

python3 VSIM.py

Follow the on-screen prompts to initialize the simulation and control the vehicles.