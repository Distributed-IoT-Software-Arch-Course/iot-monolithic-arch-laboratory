import json


class MessageDescriptor:

    def __init__(self, timestamp, data_type, value):
        self.timestamp = timestamp
        self.data_type = data_type
        self.value = value

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
