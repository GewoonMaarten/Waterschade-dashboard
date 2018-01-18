class Device:
    'An Class which defines an physical Device which is use to measure water damage .'
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status