from abc import ABC, abstractmethod 
from VehicleStatus import VehicleStatus
import time
import json
from pynput.keyboard import Key, Listener
import keyboard
import threading
import requests
import ast

class Vehicle(ABC):
    def __init__(self, tracking_number, current_location, type, license_plate):
        self.tracking_number = tracking_number
        self.current_location = current_location
        self.status = VehicleStatus.IDLE
        self.type = type
        self.route = []
        self.license_plate = license_plate
        self.paused = False
        self.thread = None
        self.alive = True
        # self.statusAPI = False
        self.battery_level = 100

    def start(self):
        self.thread = threading.Thread(target=self.awaken)
        self.thread.start()

    def pause(self):
        self.paused = True
        self.status = VehicleStatus.STOPPED

    def resume(self):
        self.paused = False
        self.status = VehicleStatus.EN_ROUTE

    @abstractmethod
    def getTrackingNumber(self):
        pass
    @abstractmethod
    def setTrackingNumber(self, tracking_number):
        pass
    @abstractmethod
    def getRoute(self):
        pass
    @abstractmethod
    def setRoute(self, route):
        pass
    @abstractmethod
    def getStatus(self):
        pass
    @abstractmethod
    def setStatus(self, status):
        pass
    @abstractmethod
    def getCurrentLocation(self):
        pass
    @abstractmethod
    def setCurrentLocation(self, current_location):
        pass
    @abstractmethod
    def getType(self):
        pass
    @abstractmethod
    def setType(self, type):
        pass
    @abstractmethod
    def getLicensePlate(self):
        pass
    @abstractmethod
    def setLicensePlate(self, license_plate):
        pass
    
    def set_battery_level(self, new_battery_level: int) -> None:
        self.battery_level = new_battery_level

    def get_battery_level(self) -> int:
        return self.battery_level

    def unpack_route(self, string_route):
        list_route = ast.literal_eval(string_route)
        return list_route

    def awaken(self):
        self.alive = True
        while self.alive == True:
            self.send_status()

            if self.status == VehicleStatus.IDLE:
                self.get_route() # constantly checks if there is a job available
            
            # Traversing Route:
            route_length: int = len(self.route)
            if self.status == VehicleStatus.EN_ROUTE:
                for i in range(route_length):
                    print(f"index: {i}")
                    self.send_status()
                    print(f"\nVehicle {self.license_plate}\n--------------\n{self.status}\n{self.current_location}\n")
                    at_end_of_route: bool = (i == route_length - 1)
                    print(f"At the end of route: {at_end_of_route}")
                    print(f"Route length: {route_length}")
                    if at_end_of_route:
                        self.status = VehicleStatus.COMPLETED
                        self.send_status()
                        time.sleep(5)
                        print(f"Vehicle {self.license_plate} has completed its trip!")
                        print(f"Vehicle {self.license_plate} will now be waiting for another job...")
                        self.status = VehicleStatus.IDLE
                        
                    else:
                        self.current_location = self.route[i+1]
                        time.sleep(5)

            # Delay Sending Status
            time.sleep(5)

    def sleep(self):
        self.alive = False

    def send_status(self):
        form_data = {
            'vehicle_id': self.license_plate,
            'vehicle_type': self.getType(),
            'latitude': str(self.current_location[1]),
            'longitude': str(self.current_location[0]),
            'status': self.status.name, 
            'battery': self.battery_level
        }

        try:
            base_url = "https://team-12.supply.seuswe.rocks" # production testing
            # base_url = "http://localhost:9000" # local testing
            response = requests.post(f"{base_url}/supply-services/fleet/update-data/", data=form_data)
            
            if response.status_code < 200 and response.status_code >= 300:
                print(f'Request failed with status code: {response.status_code}')

        except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
            print('An error occurred during the request:', e)

    def get_route(self):
        """
        Asks for a route from supply cloud
        """

        form_data = {
            'vehicle_id': self.license_plate
        }

        try:
            base_url = "https://team-12.supply.seuswe.rocks" # production testing
            # base_url = "http://localhost:9000" # local testing
            response = requests.post(f"{base_url}/supply-services/fleet/get-route/", data=form_data)

            if response.status_code >= 200 and response.status_code < 300:
                data = response.json()
                has_trip: bool = data.get("has_trip")

                if has_trip:
                    route = data.get("route")
                    self.route = route
                    #TODO: Implement Waypoint stops
                    self.status = VehicleStatus.EN_ROUTE
            else:
                print(f'Request failed with status code: {response.status_code}')

        except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
            print('An error occurred during the request:', e)