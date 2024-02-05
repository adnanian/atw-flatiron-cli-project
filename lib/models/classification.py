# lib/models/classification.py
from models.__init__ import (CURSOR, execute_and_commit)
from models.model_helpers import (validate_attribute_text)


class Classification:
    all = {}
    MODEL_NAME = "classification"

    def __init__(self, name, geographic_locaiton, id=None):
        """ Create an instance of Classification.

        Args:
            name (str): the name.
            geographic_locaiton (str): the main geographic location of the language classification.
            id (int, optional): the id number represented in the database. Defaults to None.
        """
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
        """ Creates the classifciations table in the language_categories database."""
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
        """ Deletes the classifications table from the language_categories database. """
        sql = """
            DROP TABLE IF EXISTS classifications
        """
        
        execute_and_commit(sql)
        
    def save(self):
        """ Adds a new row to the classifications table by inserting the property values of the instance this method was called on into the table. """
        sql = """
            INSERT INTO classifications (name, geographic_location)
            VALUES (?, ?)
        """
        
        execute_and_commit(sql, (self.name, self.geographic_location))

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, name, geographic_locaiton):
        """ First, creates a new instance of Classification.
            Then, creates a new row consisting of that instance's property values.
            Finally, adds that row to the classifications table.

        Args:
            name (_type_): the name.
            geographic_locaiton (_type_): the main geographic location of the language classification.

        Returns:
            _type_: _description_
        """
        classification = cls(name, geographic_locaiton)
        classification.save()
        return classification
    
    def update(self):
        """ Updates the table row corresponding to the current Classification instance. """
        sql = """
            UPDATE classifications
            SET name = ?, geographic_location = ?
            WHERE id = ?
        """
        execute_and_commit(sql, (self.name, self.geographic_location, self.id))
        
    def delete(self):
        """ Deletes the table row corresponding to the current Classification instance, 
        delete the dictionary entry, and reassign the id attribute to None."""
        
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
        """Return a Classification object having the attribute values from the table row.

        Args:
            row (database row): the row from the database

        Returns:
            the Classification object matching that row if it exists; None otherwise.
        """
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
        """ Returns a list containing the Classification object per row in the table. """
        sql = """
            SELECT *
            FROM classifications
        """
        
        rows = CURSOR.execute(sql).fetchall()
        
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return a Classification object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM classifications
            WHERE id = ?
        """
        
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """Return a Classification object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM classifications
            WHERE name is ?
        """
        
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def languages(self):
        """ Returns a list of languages associated with the classification."""
        from models.language import Language
        sql = """
            SELECT *
            FROM languages
            WHERE classification_id = ?
        """
        CURSOR.execute(sql, (self.id,),)
        rows = CURSOR.fetchall()
        return [
            Language.instance_from_db(row) for row in rows
        ]
    
    @classmethod
    def get_longest_attribute_length(cls, attribute_name):
        """ Returns the longest length among all the values of a table in a given column in the classifications table."""
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
        """ Returns the names of columns in the classification table. """
        sql = """
            PRAGMA table_info(classifications)
        """
        columns = CURSOR.execute(sql).fetchall()
        return columns
       
    @classmethod
    def row_count(cls):
        """ Returns the number of rows in the classifications table. """
        sql = """
            SELECT COUNT(*) FROM classifications
        """
        row_count = CURSOR.execute(sql).fetchone()
        return row_count
        