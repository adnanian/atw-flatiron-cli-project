from models.__init__ import CURSOR, execute_and_commit
from models.model_helpers import validate_attribute_text, format_string_cell
from models.classification import Classification


class Language:
    all = {}

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
            self._status = status
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
