#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.classification import Classification
from models.language import Language
import ipdb

a = Classification.get_longest_attribute_length('name')
b = Classification.get_longest_attribute_length('geographic_location')

c = Language.get_longest_attribute_length('name')
d = Language.get_longest_attribute_length('number_of_speakers')
e = Language.get_longest_attribute_length('country_of_origin')
f = Language.get_longest_attribute_length('status')

ipdb.set_trace()
