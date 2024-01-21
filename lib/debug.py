#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.classification import Classification
import ipdb

c1 = Classification("Semitic", "Middle East", 1)
c2 = Classification("Slavic", "Eastern Europe", 2)

Classification.table_heading()
print(c1)
print(c2)

ipdb.set_trace()
