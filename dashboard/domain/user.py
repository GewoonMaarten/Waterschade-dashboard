class User:
    'The class that residents use to login.'
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password