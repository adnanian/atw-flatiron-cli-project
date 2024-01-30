#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.classification import Classification
from models.language import Language
import ipdb

classification = Classification.find_by_id(1)

ipdb.set_trace()
