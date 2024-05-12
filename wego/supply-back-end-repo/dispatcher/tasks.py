from .models import Dispatcher, Trip
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_assign_vehicles, 'interval', seconds=5)
    scheduler.start()

def check_and_assign_vehicles():
    dispatcher = Dispatcher()
    unassigned_trips = Trip.objects.filter(vehicle_id__isnull=True)
    for trip in unassigned_trips:
        dispatcher.assign_vehicle_to_trip(trip)
