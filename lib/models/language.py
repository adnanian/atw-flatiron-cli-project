from models.__init__ import CURSOR, execute_and_commit
from models.model_helpers import validate_attribute_text, format_string_cell


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
