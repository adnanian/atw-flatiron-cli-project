# lib/models/classification.py
from models.__init__ import (CURSOR, execute_and_commit)
from models.model_helpers import (validate_attribute_text)


class Classification:
    all = {}

    def __init__(self, name, geographic_locaiton, id=None):
        self.id = id
        self.name = name
        self.geographic_location = geographic_locaiton
        
    def __repr__(self):
        return str(self.__dict__)

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
                name VARCHAR(24) UNIQUE,
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
        """ TODO """
        classification = cls(name, geographic_locaiton)
        classification.save()
        return classification
    
    def update(self):
        """ TODO """
        sql = """
            UPDATE classifications
            SET name = ?, geographic_location = ?
            WHERE id = ?
        """
        execute_and_commit(sql, (self.name, self.geographic_location, self.id))
        
    def delete(self):
        """ TODO """
        
        sql = """
            DELETE FROM classifications
            WHERE id = ?
        """
        
        execute_and_commit(sql, (self.id,))
        
        del type(self).all[self.id]
        self.id = None
    
    # Review with instructor
    @classmethod
    def instance_from_db(cls, row):
        """ TODO """
        # Check the classification for an existing instance using the row's primary key
        classification = cls.all.get(row[0])
        if classification:
            # ensure attributes match row values in case local instance was modified
            classification.name = row[1]
            classification.geographic_locaiton = row[2]
        else:
            # not in classification, create new instance and add to dictionary
            classification = cls(row[1], row[2])
            classification.id = row[0]
            cls.all[classification.id] = classification
        return classification
            
    @classmethod
    def get_all(cls):
        """ TODO """
        sql = """
            SELECT *
            FROM classifications
        """
        
        rows = CURSOR.execute(sql).fetchall()
        
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """ TODO """
        sql = """
            SELECT *
            FROM classifications
            WHERE id = ?
        """
        
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """ TODO """
        sql = """
            SELECT *
            FROM classifications
            WHERE name is ?
        """
        
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def languages(self):
        """ TODO """
        pass
    
    @classmethod
    def get_longest_attribute_length(cls, attribute_name):
        """ TODO """
        if attribute_name in ("name", "geographic_location"):
            sql = f"""
                SELECT length({attribute_name})
                FROM classifications
                ORDER BY length({attribute_name}) DESC
                LIMIT 1;
            """
            row = CURSOR.execute(sql).fetchone()
            return row
        else:
            raise ValueError("Attribute name must be a valid table column.")
        
    @classmethod
    def get_column_names(cls):
        """ TODO """
        sql = """
            PRAGMA table_info(classifications)
        """
        columns = CURSOR.execute(sql).fetchall()
        return columns
       
        