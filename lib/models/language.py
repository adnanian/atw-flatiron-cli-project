from models.__init__ import CURSOR, execute_and_commit
from models.model_helpers import validate_attribute_text
from models.classification import Classification


class Language:
    all = {}
    MODEL_NAME = "language"
    STATUSES = ["LIVING", "ENDANGERED", "DEAD", "EXTINCT"]

    def __init__(
        
        self,
        name,
        number_of_speakers,
        country_of_origin,
        status,
        classification_id,
        id=None,
    ):
        """ Create an instance of Language.

        Args:
            name (str): the name.
            number_of_speakers (int): the total number of living speakers (both native and non-native).
            country_of_origin (str): the country the language originated from.
            status (str): the status - must be one of 4 values: [LIVING, ENDANGERED, DEAD, OR EXTINCT]
            classification_id (int): foreign key for the languages table.
            id (int, optional): the id number represented in the languages table in the database. Defaults to None.. Defaults to None.
        """
        self.id = id
        self.name = name
        self.number_of_speakers = number_of_speakers
        self.country_of_origin = country_of_origin
        self.status = status
        self.classification_id = classification_id


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        validate_attribute_text(name, "name")
        self._name = name

    @property
    def number_of_speakers(self):
        return self._number_of_speakers

    @number_of_speakers.setter
    def number_of_speakers(self, number_of_speakers):
        self._number_of_speakers = number_of_speakers

    @property
    def country_of_origin(self):
        return self._country_of_origin

    @country_of_origin.setter
    def country_of_origin(self, country_of_origin):
        validate_attribute_text(country_of_origin, "country of origin")
        self._country_of_origin = country_of_origin

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if isinstance(status, str) and status.upper() in Language.STATUSES:
            self._status = status.upper()
        else:
            raise ValueError(
                "Status must be one of the listed values: ", Language.STATUSES
            )

    @property
    def classification_id(self):
        return self._classification_id

    @classification_id.setter
    def classification_id(self, classification_id):
        if type(classification_id) is int and Classification.find_by_id(
            classification_id
        ):
            self._classification_id = classification_id
        else:
            raise ValueError(
                "classification_id must reference a department in the database"
            )

    @classmethod
    def create_table(cls):
        """Creates the languages table in the language_categories database."""
        sql = """
            CREATE TABLE languages(
                id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE,
                number_of_speakers UNSIGNED INT,
                country_of_origin VARCHAR(50),
                status TEXT,
                classification_id INTEGER,
                FOREIGN KEY (classification_id) REFERENCES classifications(id)
            );
        """
        execute_and_commit(sql)

    @classmethod
    def drop_table(cls):
        """Deletes the languages table from the language_categories database."""
        sql = """
            DROP TABLE IF EXISTS languages
        """

        execute_and_commit(sql)

    def save(self):
        """Adds a new row to the languages table by inserting the attribute values of the instance this method was called on into the table."""
        sql = """
            INSERT INTO languages (name, number_of_speakers, country_of_origin, status, classification_id)
            VALUES (?, ?, ?, ?, ?)
        """

        execute_and_commit(
            sql,
            (
                self.name,
                self.number_of_speakers,
                self.country_of_origin,
                self.status,
                self.classification_id,
            )
        )

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(
        cls, name, number_of_speakers, country_of_origin, status, classification_id
    ):
        """First, creates a new instance of Language.
            Then, creates a new row consisting of that instance's property values.
            Finally, adds that row to the languages table.

        Args:
            name (str): the name.
            number_of_speakers (int): the total number of living speakers (both native and non-native).
            country_of_origin (str): the country the language originated from.
            status (str): the status - must be one of 4 values: [LIVING, ENDANGERED, DEAD, OR EXTINCT]
            classification_id (int): foreign key for the languages table.

        Returns:
            Language: the created instance of Language.
        """
        language = cls(
            name, number_of_speakers, country_of_origin, status, classification_id
        )
        language.save()
        return language

    def update(self):
        """Updates the table row corresponding to the current Language instance."""
        sql = """
            UPDATE languages
            SET name = ?, number_of_speakers = ?, country_of_origin = ?, status = ?, classification_id = ?
            WHERE id = ?
        """
        execute_and_commit(
            sql,
            (
                self.name,
                self.number_of_speakers,
                self.country_of_origin,
                self.status,
                self.classification_id,
                self.id
            )
        )

    def delete(self):
        """TODO"""

        sql = """
            DELETE FROM languages
            WHERE id = ?
        """

        execute_and_commit(sql, (self.id,))

        del type(self).all[self.id]
        self.id = None

    # Review with instructor
    @classmethod
    def instance_from_db(cls, row):
        """Return a Language object having the attribute values from the table row.

        Args:
            row (_type_): _description_

        Returns:
            _type_: the Language object matching that row if it exists; None otherwise.
        """
        # Check the language for an existing instance using the row's primary key
        language = cls.all.get(row[0])
        if language:
            # ensure attributes match row values in case local instance was modified
            language.name = row[1]
            language.number_of_speakers = row[2]
            language.country_of_origin = row[3]
            language.status = row[4]
            language.classification_id = row[5]
        else:
            # not in language, create new instance and add to dictionary
            language = cls(row[1], row[2], row[3], row[4], row[5])
            language.id = row[0]
            cls.all[language.id] = language
        return language

    @classmethod
    def get_all(cls):
        """Returns a list containing the Language object per row in the table. """
        sql = """
            SELECT *
            FROM languages
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Language object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM languages
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Language object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM languages
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def get_longest_attribute_length(cls, attribute_name):
        """ Returns the longest length among all the values of a table in a given column in the languages table. """
        if attribute_name in (column_names := ("name", "number_of_speakers", "country_of_origin", "status", "classification")):
            sql = ""
            if (attribute_name == column_names[1]):
                sql = """
                    SELECT length(printf("%,d", number_of_speakers))
                    FROM languages
                    ORDER BY number_of_speakers DESC
                    LIMIT 1;
                """
            elif (attribute_name == column_names[-1]):
                return Classification.get_longest_attribute_length("name")
            else:
                sql = f"""
                    SELECT length({attribute_name})
                    FROM languages
                    ORDER BY length({attribute_name}) DESC
                    LIMIT 1;
                """
            
            row = CURSOR.execute(sql).fetchone()
            return row
        else:
            raise ValueError("Attribute name must be a valid table column.")

    @classmethod
    def get_column_names(cls):
        """ Returns the names of columns in the languages table. """
        sql = """
            PRAGMA table_info(languages)
        """
        columns = CURSOR.execute(sql).fetchall()
        return columns
    
    @classmethod
    def row_count(cls):
        """ Returns the number of rows in the languages table. """
        sql = """
            SELECT COUNT(*) FROM languages
        """
        row_count = CURSOR.execute(sql).fetchone()
        return row_count