import random
import time
import threading
from Car import Car
from VehicleStatus import VehicleStatus

def stopOneRandomVehicle(numOfInstances, carInstances):
    
    #pick random vehicle to stop after 5 seconds of starting their route
    time.sleep(2)
    random_vehicle_id = random.randint(0, numOfInstances-1)
    print()
    print(f"Stopping Vehicle {random_vehicle_id}...")
    print()
    carInstances[random_vehicle_id].stop()

def main():

    #TO DO
    #   - USE THAT TOKEN WITH THIS HTTP API ENDPOINT https://api.mapbox.com/{endpoint}?access_token={your_access_token}
    # ask for token from ricky

    print("Starting Simulation...")

    numOfInstances = int(input("How Many Vehicles Instances Would You Like To Make: "))
    current_location = [30.228130, -97.754333]
    route = [[30.228130, -97.754333], [30.234454, -97.756813],[30.242017, -97.759734], [30.254596, -97.752356]]
    year = 1999
    license_plate = "ABC123"
    carInstances = []
    threads = []
    
    for i in range(numOfInstances):
        carInstance = Car(license_plate, current_location[0], current_location[1],year)
        thread = threading.Thread(target=carInstance.awaken) # Pass the method reference, not the call
        carInstances.append(carInstance)
        threads.append(thread) # Store Threads to be used to wait for threads to complete
        thread.start()  # Start the thread
        
    # Optionally, wait for all threads to complete onto the main thread
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()