# lib/models/classification.py
from models.__init__ import CURSOR, CONN
from models.model_helpers import (
    validate_attribute_text,
    format_string_cell
)



class Classification:
    all = {}
    
    def __init__(self, name, geographic_locaiton, id=None):
        self.id = id
        self.name = name
        self.geographic_location = geographic_locaiton
        
    def __repr__(self):
        return f" {'{:0>2}'.format(self.id)} | {format_string_cell(self.name)} | {self.geographic_location} "
        
    @classmethod
    def table_heading(cls):
        pass
        title = "Language Classifications"
        header = f" id | {format_string_cell('name')} | geographic_location "
        line = '-' * len(header)
        print(title)
        print(header)
        print(line)
    
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