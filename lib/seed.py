from models.classification import Classification
from models.language import Language

# Drop table to create new seed
Classification.drop_table()
Language.drop_table()

# Create new tables
Classification.create_table()
Language.create_table()

# Populate Classification data
Classification.create("Semitic", "Middle East")
Classification.create("Slavic", "Eastern Europe")
Classification.create("Romance", "Worldwide")
Classification.create("Germanic", "Western Europe / Worldwide")

# Populate Language data
Language.create("English", 1456000000, "United Kingdom", "Living", 4)
Language.create("Spanish", 559000000, "Spain", "Living", 3)
Language.create("French", 310000000, "France", "Living", 3)
Language.create("Arabic (MSA)", 274000000, "Saudi Arabia", "Living", 1)
Language.create("Portuguese", 264000000, "Portugal", "Living", 3)
Language.create("Russian", 255000000, "Russia", "Living", 2)
Language.create("Aramaic", 850000, "Syria", "Endangered", 1)
Language.create("Latin", 3300000, "Italy", "Dead", 3)
Language.create("Aramaic", 0, "Iraq", "Extinct", 1)