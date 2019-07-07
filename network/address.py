import json


class Address:

    def __init__(self, host: str = None, port: int = None, json_data=None) -> None:
        if not json_data:
            self.host = host
            self.port = port
        else:
            self.host = json_data['host']
            self.port = json_data['port']

    def __eq__(self, other) -> bool:
        return self.host == other.host and self.port == other.port

    def __ne__(self, other) -> bool:
        return self.host != other.host or self.port != other.port

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self) -> str:
        return f'{self.host}:{self.port}'
