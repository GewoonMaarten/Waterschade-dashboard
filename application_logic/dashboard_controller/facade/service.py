import os
import sqlite3

from data.dashboard_persistency.facade.service import Service as Persistency_service

PERSISTENCY_SERVICE = Persistency_service('./database.db')

class Service(object):
    """Service for the sensor package to interact with"""

    def add_new_device(self, device_id, name=None):
        PERSISTENCY_SERVICE.add_device(device_id)

    def report_water_damage(self, device_id):
        pass

    def check_if_sensor_present(self, device_id):
        exists = PERSISTENCY_SERVICE.get_device(device_id)

        if exists is None:
            return False
        return True
