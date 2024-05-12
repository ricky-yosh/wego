from VehicleStatus import VehicleStatus
from Vehicle import Vehicle
import time

class Car(Vehicle):
    def __init__(self, tracking_number, current_location, year, license_plate):
        super().__init__(tracking_number, current_location, "CAR", license_plate)
        self.year = year
        self.license_plate = license_plate
        self.type = "CAR"
        self.stop_requested = False

    def getTrackingNumber(self):
        return self.tracking_number
    
    def setTrackingNumber(self, tracking_number):
        self.tracking_number = tracking_number

    def getRoute(self):
        return self.route
    
    def setRoute(self, route):
        self.route = route

    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status

    def getCurrentLocation(self):
        return self.current_location
    
    def setCurrentLocation(self, current_location):
        self.current_location = current_location

    def setLicensePlate(self, license_plate):
        self.license_plate = license_plate

    def getLicensePlate(self):
        return self.license_plate
    
    def setYear(self, year):
        self.year = year

    def getYear(self):
        return self.year
    
    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type
    
    # def updateCarLocation(self):
    #     self.status = VehicleStatus.EN_ROUTE
    #     route = self.getRoute()  # Get the route once before the loop

    #     for next_location in route:
    #         if self.stop_requested:
    #             break  # Exit the loop if a stop has been requested

    #         time.sleep(5)  # Simulate time passing between locations
    #         self.current_location = next_location
    #         print(f"Moving to: {self.current_location}, current car status: {self.status}")

    #     if not self.stop_requested:
    #         # Only update the status to COMPLETED if the stop wasn't requested
    #         self.status = VehicleStatus.COMPLETED
    #     else:
    #         # Only update the status to STOPPED if the stop was requested
    #         self.status = VehicleStatus.STOPPED

    #     print(f"Final Car route: {self.current_location}, current car status: {self.status}")

    # def returnCurrentLocation(self):
    #     return self.current_location
            
    # def stop(self):
    #     self.stop_requested = True  # Method to set the flag

    # def restart(self):
    #     self.stop_requested = False

    def awaken(self):
        return super().awaken()
    
    def sleep(self):
        return super().sleep()
    
    def unpack_route(self, route):
        return super().unpack_route(route)