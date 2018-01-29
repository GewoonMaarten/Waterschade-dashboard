

class Service(object):
    """Service for the sensor package to interact with"""

    def __init__(self):
        pass

    def add_new_device(self, id, name="water_sensor"):
        print(id, name)

    def report_water_damage(self, id):
        pass

    def check_if_sensor_present(self, id):
        # true or false
        pass

    