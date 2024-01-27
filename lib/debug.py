#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.classification import Classification
from models.language import Language
import ipdb

print(Classification.get_longest_attribute_length('name'))
print(Classification.get_longest_attribute_length('geographic_location'))

print(Language.get_longest_attribute_length('name'))
print(Language.get_longest_attribute_length('number_of_speakers'))
print(Language.get_longest_attribute_length('country_of_origin'))
print(Language.get_longest_attribute_length('status'))

ipdb.set_trace()
