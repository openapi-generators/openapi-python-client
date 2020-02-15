from dataclasses import dataclass

@dataclass
class Client:
    """ A class for keeping track of data related to the API """
    base_url: str
