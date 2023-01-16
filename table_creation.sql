-- Active: 1673871752427@@127.0.0.1@3306@clean_greyhound_data
CREATE TABLE track (
    track_id INT AUTO_INCREMENT,
    location VARCHAR(32),
    distance INT,
    PRIMARY KEY (track_id)
);

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

CREATE TABLE dog (
    dog_id VARCHAR(32),
    PRIMARY KEY (dog_id)
);

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

CREATE TABLE std_time (
    track_id INT,
    grade VARCHAR(64),
    std_time FLOAT,
    std_sect_time FLOAT,
    PRIMARY KEY (track_id, grade),
    FOREIGN KEY (track_id) 
        REFERENCES track(track_id)
);

