#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.classification import Classification
import ipdb

c1 = Classification("Semitic", "Middle East")
c2 = Classification(123, "Eastern Europe")

ipdb.set_trace()
