import random
import time
import threading
from threading import active_count
from Car import Car
from VehicleStatus import VehicleStatus
import keyboard # type: ignore
import requests # type: ignore

url = "https://team-12.supply.seuswe.rocks/supply-services/fleet/add-vehicle/"

def is_key_pressed():
    return keyboard.is_pressed("s") or keyboard.is_pressed("c") or keyboard.is_pressed("k") or keyboard.is_pressed("r") or keyboard.is_pressed("b")

def clear_input():
    keyboard.press_and_release('enter')
    input()

def create_license_plate(index):
    index += 1
    license_plate = "TEST-"
    if index < 10:
        license_plate += "000" + str(index)
    elif index < 100:
        license_plate += "00" + str(index)
    elif index < 1000:
        license_plate += "0" + str(index)
    elif index < 10000:
        license_plate += str(index)
    else:
        license_plate = "XXXX-XXXX"
    return license_plate

def create_random_location():
    latitude = round(random.uniform(30.150, 30.450), 6)
    longitude = round(random.uniform(-97.450, -97.900), 6)
    location = [longitude, latitude]
    return(location)

# NOT USING YET
def add_vehicle_to_cloud(vehicle):
    form_data = {
            'vehicle_id': vehicle.getLicensePlate(),
            'vehicle_type': vehicle.getType()
        }
    
    try:
        response = requests.post(url, data=form_data)
        
        if response.status_code >= 200 and response.status_code <300:
            print(response.text)
        elif response.status_code == 409:
            print("Vehicle already existent in Supply Cloud")
        else:
            print(f'Request failed with status code: {response.status_code}')

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print('An error occurred during the request:', e)


def main():
    print("Press S and then enter the car number to Stop a car")
    print("Press H to change heartbeat status")
    print("Press C and then enter the necessary information to Create a car")
    print("Press K to Kill the program")
    print("Press U to change vehicle battery level")
    print("Press R to Restart the program")
    print("Press B to get a Briefing of the vehicles status")
    print("\nStarting Simulation...\n")

    while True:
        input_numOfInstances = input("How Many Vehicles Instances Would You Like To Make: ")
        try:
            numOfInstances = int(input_numOfInstances)
            print(str(numOfInstances) + " car(s) created.")
            break
        except ValueError:
            print("Input not a number")

    year = 1999
    carInstances = []
    vehicle_numbers_list = []
    indexOfTheCar = 0
    program_awake = True
    
    for i in range(numOfInstances):
        license_plate = create_license_plate(i)
        current_location = create_random_location()
        carInstance = Car(i, current_location, year, license_plate)
        carInstance.start()
        carInstance.getStatus
        carInstances.append(carInstance)
        indexOfTheCar += 1
        vehicle_numbers_list.append(i + 1)
    
    while True:
        while program_awake:
            keyPressed = keyboard.read_key()
            # print(keyPressed)
            time.sleep(0.5)

            # Stop Car
            if keyPressed == "s" or keyPressed == "S" or keyPressed == 1:
                clear_input()
                # Generate a list of indices starting from 1
                car_id = input('Which car do you wish to stop? Select ' + str(vehicle_numbers_list) + '?\n')
                print("Car selected: " + car_id)
                try:
                    car_id_int = int(car_id)-1
                    if car_id_int >= 0 and car_id_int < active_count():
                        if carInstances[car_id_int].paused:
                            carInstances[car_id_int].resume()
                            print("Resuming route for car: " + car_id_int)
                        elif carInstances[car_id_int].getStatus() == VehicleStatus.EN_ROUTE:
                            carInstances[car_id_int].pause()
                            print("Pausing route for car: " + car_id_int)
                        selected_car_status: VehicleStatus = carInstances[car_id_int].getStatus()
                        print("Selected vehicle status is: " + str(selected_car_status.value))
                        keyPressed = ""
                    else:
                        print("Input out of range")
                except ValueError:
                    print("Incorrect Input")
            
            # Stop Heartbeat
            elif keyPressed == "h" or keyPressed == "H" or keyPressed == 4:
                clear_input()
                # Generate a list of indices starting from 1
                car_id = input('Which car\'s heartbeat do you want to stop? Select ' + str(vehicle_numbers_list) + '?\n')
                print("Car selected: " + car_id)
                try:
                    car_id_int = int(car_id)-1
                    if car_id_int >= 0 and car_id_int < active_count():
                        if carInstances[car_id_int].alive == True:
                            carInstances[car_id_int].sleep()
                            print("Stopping heartbeat for car: " + car_id)
                        elif carInstances[car_id_int].alive == False:
                            carInstances[car_id_int].awaken()
                            print("Resuming heartbeat for car: " + car_id)
                        selected_car_status: bool = carInstances[car_id_int].alive
                        print("Vehicle " + car_id + " sending heartbeat: " + str(selected_car_status))
                        keyPressed = ""
                    else:
                        print("Input out of range")
                except ValueError:
                    print("Incorrect Input")

            # Change Battery Level
            elif keyPressed == "u" or keyPressed == "U" or keyPressed == 32:
                clear_input()
                # Generate a list of indices starting from 1
                car_id = input('Which car would you like to change the battery level? Select ' + str(vehicle_numbers_list) + '?\n')
                print("Car selected: " + car_id)
                try:
                    car_id_int = int(car_id)-1
                    if car_id_int >= 0 and car_id_int < active_count():
                        new_battery_level = input("What battery level would you like to set vehicle " + car_id + " to? (0-100) ")
                        carInstances[car_id_int].set_battery_level(new_battery_level)
                        print("Vehicle " + car_id + " battery level: " + carInstances[car_id_int].get_battery_level() + "%")
                    else:
                        print("Input out of range")
                except ValueError:
                    print("Incorrect Input")

            # Create Car
            elif keyPressed == "c" or keyPressed == "C" or keyPressed == 8:
                clear_input()
                print("Creating a car, enter the following information:\n\n")
                car_id = indexOfTheCar

                randomize_location = input("Do you wish to randomize the car location(around the Austin area)? (n for no)")
                if randomize_location == 'n':
                    current_location_latitude = input('What is the current latitude location of the car?\n')
                    current_location_longitude = input('What is the current longitude location of the car?\n')
                    car_current_location = [current_location_latitude, current_location_longitude]
                else:
                    car_current_location = create_random_location()
                
                car_year = input('What is the year of the car?\n')

                randomize_license_plate = input("Do you wish to randomize the car license plate? (n for no)")
                if randomize_license_plate == 'n':
                    car_license_plate = input('What is the license plate of the car?\n')
                else:
                    car_license_plate = create_license_plate(indexOfTheCar)

                carInstance = Car(car_id, car_current_location, car_year, car_license_plate)
                carInstance.start()
                carInstances.append(carInstance)
                
                print ("\nCreation of the Car...\n")
                
                indexOfTheCar += 1
                keyPressed = ""

            # Briefing of Vehicles Information
            elif keyPressed == "b" or keyPressed == "B" or keyPressed == 11:
                clear_input()
                print(("Briefing of the fleet").center(100, '-'))
                print("\n")
                index = 0
                for car in carInstances:
                    index += 1
                    print((f"Vehicle {index}").center(100, ' '))
                    print((f"Vehicle Type : {car.getType()}").center(100, ' '))
                    print((f"Tracking number : {car.getTrackingNumber()}").center(100, ' '))
                    print((f"License plate : {car.getLicensePlate()}").center(100, ' '))
                    print((f"Status : {car.getStatus().name}").center(100, ' '))
                    print((f"Location : {car.getCurrentLocation()}").center(100, ' '))
                    print((f"Battery Level : {str(car.get_battery_level())}%").center(100, ' '))
                    print((f"Sending Heartbeat : {car.alive}").center(100, ' '))
                    print("\n")
                keyPressed = ""

            # Kill Vehicle Run
            elif keyPressed == "k" or keyPressed == "K" or keyPressed == 40:
                clear_input()
                print("Killing the run...")
                program_awake = False
                for car in carInstances:
                    car.sleep()
                keyPressed = ""
                break

        # Restart Program
        if keyPressed == "r" or keyPressed == "R" or keyPressed == 15:
            clear_input()
            print("Restart of the program...")
            main()

if __name__ == '__main__':
    main()
