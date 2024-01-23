# lib/models/classification.py
from models.__init__ import (CURSOR, execute_and_commit)
from models.model_helpers import (validate_attribute_text, format_string_cell)


class Classification:
    all = {}

    def __init__(self, name, geographic_locaiton, id=None):
        self.id = id
        self.name = name
        self.geographic_location = geographic_locaiton

    def __repr__(self):
        return f" {'{:0>2}'.format(self.id)} | {format_string_cell(self.name)} | {self.geographic_location} "

    def return_as_table_row(self):
        """ Return a representation of the Classifications object as a table row of data. (Id attribute not included.) """
        return f" {format_string_cell(self.name)} | {self.geographic_location} "

    @classmethod
    def table_heading(cls):
        pass
        title = "Language Classifications"
        header = f" {format_string_cell('name')} | geographic_location "
        line = "-" * len(header)
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

    @classmethod
    def create_table(cls):
        """TODO"""
        sql = """
            CREATE TABLE classifications(
                id INTEGER PRIMARY KEY,
                name VARCHAR(24),
                geographic_location TEXT
            );
        """
        execute_and_commit(sql)
        
    @classmethod
    def drop_table(cls):
        """ TODO may not need to use. Will need to see. """
        sql = """
            DROP TABLE IF EXISTS classifications
        """
        
        execute_and_commit(sql)
        
    def save(self):
        """ TODO """
        sql = """
            INSERT INTO classifications (name, geographic_location)
            VALUES (?, ?)
        """
        
        execute_and_commit(sql, (self.name, self.geographic_location))

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, name, geographic_locaiton):
        pass