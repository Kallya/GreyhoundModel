-- Active: 1672317998122@@127.0.0.1@3306@race_data
DELETE FROM dog_race_result;
DELETE FROM race_record;
DELETE FROM dog;
DELETE FROM track;
DELETE FROM std_time;
CREATE TABLE track (
    track_id INT AUTO_INCREMENT,
    location VARCHAR(32) NOT NULL,
    distance INT NOT NULL,
    PRIMARY KEY (track_id)
);

SELECT * FROM race_record_temp WHERE date < "2022-12-1";

SELECT * FROM track;

SELECT * FROM dog_race_result;
SELECT SELECT dog_id, race_id

SELECT STDDEV(b.weight) 
FROM (SELECT race_id, date FROM race_record_temp WHERE date < "2022-12-09") a
INNER JOIN dog_race_result_temp b 
WHERE b.dog_id = "AARON ALPACA" AND b.race_id = a.race_id
LIMIT 3;

SELECT * FROM dog_race_result_temp WHERE dog_id = "AARON ALPACA";

CREATE TABLE race_record (
    race_id INT AUTO_INCREMENT,
    date DATE,
    track_id INT,
    grade VARCHAR(64),
    race_no INT,
    runner_num INT,
    PRIMARY KEY (race_id),
    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
);
SELECT * FROM dog_race_result_temp ORDER BY time DESC;

SELECT COUNT(*) / 0 FROM dog_race_result_temp;
CREATE TABLE race_record_temp (
    race_id INT,
    date DATE,
    track_id INT,
    grade VARCHAR(64),
    race_no INT,
    runner_num INT,
    PRIMARY KEY (race_id),
    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
);

SELECT * FROM dog_race_result_temp WHERE dog_id = "AARON ALPACA";

CREATE TABLE dog (
    dog_id VARCHAR(32),
    type VARCHAR(32),
    starts INT,
    wins INT,
    places INT,
    win_rate FLOAT,
    place_rate FLOAT,
    PRIMARY KEY (dog_id)
);
SELECT * FROM dog;

-- junction table for dog and race_record
CREATE TABLE dog_race_result (
    race_id INT,
    dog_id VARCHAR(64),
    box INT,
    place INT,
    time FLOAT,
    sect_time FLOAT,
    adjusted_time FLOAT,
    adjusted_sect_time FLOAT,
    weight FLOAT,
    bsp FLOAT,
    PRIMARY KEY (race_id, dog_id),
    FOREIGN KEY (race_id)
        REFERENCES race_record(race_id),
    FOREIGN KEY (dog_id)
        REFERENCES dog(dog_id)
);

SELECT * FROM dog_race_result;
CREATE TABLE dog_race_result_temp ( 
    race_id INT,
    dog_id VARCHAR(64),
    box INT,
    place INT,
    time FLOAT,
    sect_time FLOAT,
    adjusted_time FLOAT,
    adjusted_sect_time FLOAT,
    weight FLOAT,
    bsp FLOAT,
    PRIMARY KEY (race_id, dog_id),
    FOREIGN KEY (race_id)
        REFERENCES race_record_temp(race_id),
    FOREIGN KEY (dog_id)
        REFERENCES dog(dog_id)
);

CREATE TABLE std_time (
    track_id INT,
    grade VARCHAR(64),
    std_time FLOAT,
    std_sect_time FLOAT,
    PRIMARY KEY (track_id, grade),
    FOREIGN KEY (track_id) 
        REFERENCES track(track_id)
);
SELECT * FROM std_time;
CREATE TABLE track_grade (
    track_id INT,
    grade VARCHAR(64)
);
 SELECT * FROM track_grade;