CREATE TABLE classifications(
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    geographic_location TEXT
);

CREATE TABLE languages(
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    number_of_speakers UNSIGNED INT,
    country_of_origin VARCHAR(50),
    status TEXT,
    classification_id INTEGER,
    FOREIGN KEY (classification_id) REFERENCES classifications(id)
);