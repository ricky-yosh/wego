import unittest
from unittest.mock import patch, MagicMock
from VehicleStatus import VehicleStatus
from Car import Car
from Vehicle import Vehicle
from VSIM import create_license_plate
import time

class testCarClass(unittest.TestCase):
 
    # def testReachedDestination(self):
    #     tracking_number = 12
    #     status = VehicleStatus.INACTIVE
    #     route = [[30.228130, -97.754333], [30.234454, -97.756813],[30.242017, -97.759734], [30.254596, -97.752356]]
    #     year = 1999
    #     license_plate = "H5FR-123F"
    #     carInstance = Car(tracking_number, None, status, route, year, license_plate)
    #     print("current Car route: ", route, "current Car status: ", status)
    #     print("starting Car....")
    #     carInstance.updateCarLocation()
    #     current_location = carInstance.returnCurrentLocation()
    #     destination = [30.254596, -97.752356] #latitude, longitude
    #     print("current_location: ",current_location)
    #     print("destination: ", destination)
    #     self.assertEquals(current_location, destination, "Car DID NOT REACH DESTINATION")
    def setUp(self):
        license_plate = create_license_plate(0)
        self.vehicle = Car(1, [30.123, -97.456], 1999, license_plate)

    def test_start(self):
        self.vehicle.start()
        self.assertTrue(self.vehicle.alive)

    def test_pause(self):
        self.vehicle.pause()
        self.assertTrue(self.vehicle.paused)
        self.assertEqual(self.vehicle.getStatus(), VehicleStatus.STOPPED)

    def test_resume(self):
        self.vehicle.resume()
        self.assertFalse(self.vehicle.paused)
        self.assertEqual(self.vehicle.getStatus(), VehicleStatus.EN_ROUTE)

    def test_getters_and_setters(self):
        self.assertEqual(self.vehicle.getTrackingNumber(), 1)
        self.assertEqual(self.vehicle.getYear(), 1999)
        self.assertEqual(self.vehicle.getType(), "CAR")
        self.assertEqual(self.vehicle.getLicensePlate(), "TEST-0001")

        self.vehicle.setTrackingNumber(2)
        self.assertEqual(self.vehicle.getTrackingNumber(), 2)

        self.vehicle.setYear(2005)
        self.assertEqual(self.vehicle.getYear(), 2005)

        self.vehicle.setType("DRONE")
        self.assertEqual(self.vehicle.getType(), "DRONE")

        self.vehicle.setLicensePlate('TEST-0002')
        self.assertEqual(self.vehicle.getLicensePlate(), 'TEST-0002')

    def test_set_route(self):
        route = [(30.123, -97.456), (30.456, -97.789), (30.789, -97.123)]
        self.vehicle.setRoute(route)
        self.assertEqual(self.vehicle.getRoute(), route)


if __name__ == '__main__':
    unittest.main()