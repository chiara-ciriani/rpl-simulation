class Message:
    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.data = data

    def get_destination(self):
        return self.destination