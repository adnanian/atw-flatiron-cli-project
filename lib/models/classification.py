# lib/models/classification.py
from models.__init__ import CURSOR, CONN
from models.model_helpers import validate_attribute_text

NAME_COL_LIMIT = 52

class Classification:
    all = {}
    
    def __init__(self, name, geographic_locaiton, id=None):
        self.id = id
        self.name = name
        self.geographic_location = geographic_locaiton
        
    def __repr__(self) -> str:
        lengths = len(str(self.id) + self.name + self.geographic_location)
        
        combined_string = ""
        return combined_string
        
    @classmethod
    def table_heading(cls):
        title = "Language Classifications"
        header = f" id | name | geographic_location "
        line = '_' * len(header)
        return title + "\n" + header + "\n" + line
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        try:
            validate_attribute_text(name, "name")
            self._name = name
        except Exception as exc:
            print(exc)
            
    @property
    def geographic_location(self):
        return self._geographic_location
    
    @geographic_location.setter
    def geographic_location(self, geographic_location):
        try:
            validate_attribute_text(geographic_location, "geographic location")
            self._geographic_location = geographic_location
        except Exception as exc:
            print(exc)