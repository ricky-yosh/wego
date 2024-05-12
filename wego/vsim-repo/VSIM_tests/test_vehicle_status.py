# test_vehicle_status.py
import sys
import os

# Add the parent directory to sys.path to find the VSIM package
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from VSIM.VehicleStatus import VehicleStatus
import pytest

def test_vehicle_statuses_exist():
    assert VehicleStatus.IDLE, "IDLE member is missing"
    assert VehicleStatus.EN_ROUTE, "EN_ROUTE member is missing"
    assert VehicleStatus.STOPPED, "STOPPED member is missing"
    assert VehicleStatus.COMPLETED, "COMPLETED member is missing"

def test_vehicle_status_values():
    assert VehicleStatus.IDLE.value == 'IDLE', "IDLE member does not have the correct value"
    assert VehicleStatus.EN_ROUTE.value == 'EN_ROUTE', "EN_ROUTE member does not have the correct value"
    assert VehicleStatus.STOPPED.value == 'STOPPED', "STOPPED member does not have the correct value"
    assert VehicleStatus.COMPLETED.value == 'COMPLETED_ROUTE', "COMPLETED member does not have the correct value"
