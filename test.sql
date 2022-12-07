-- Active: 1669859970324@@127.0.0.1@3306@test
CREATE TABLE track (
    track_id INT AUTO_INCREMENT,
    location VARCHAR(32) NOT NULL,
    distance INT NOT NULL,
    PRIMARY KEY (track_id)
);

CREATE TABLE race_record (
    race_id INT AUTO_INCREMENT,
    date DATE NOT NULL,
    track_id INT NOT NULL,
    grade VARCHAR(20) NOT NULL,
    race_no INT NOT NULL,
    runner_num INT NOT NULL,
    PRIMARY KEY (race_id),
    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
);

CREATE TABLE dog (
    dog_id VARCHAR(32),
    type VARCHAR(32),
    starts INT,
    wins INT,
    places INT,
    win_rate FLOAT,
    place_rate FLOAT,
    PRIMARY KEY (dog_id),
);

-- junction table for dog and race_record
CREATE TABLE dog_race_result (
    race_id INT,
    dog_id VARCHAR(32),
    box INT NOT NULL,
    place INT NOT NULL,
    time FLOAT NOT NULL,
    sect_time FLOAT NOT NULL,
    adjusted_time FLOAT,
    adjusted_sect_time FLOAT,
    weight FLOAT,
    pir VARCHAR(6),
    PRIMARY KEY (race_id, dog_id),
    FOREIGN KEY (race_id)
        REFERENCES race_record(race_id),
    FOREIGN KEY (dog_id)
        REFERENCES dog(dog_id)
);

CREATE TABLE box_stats (
    dog_id VARCHAR(32),
    track_location VARCHAR(32) NOT NULL,
    box INT NOT NULL,
    starts INT,
    win_rate FLOAT,
    place_rate FLOAT,
    PRIMARY KEY (dog_id, track_location, box),
    FOREIGN KEY (dog_id)
        REFERENCES dog(dog_id)
);

CREATE TABLE track_stats (
    dog_id VARCHAR(32),
    track_id INT,
    starts INT,
    wins INT,
    places INT,
    win_rate FLOAT,
    place_rate FLOAT,
    best_time FLOAT,
    best_split FLOAT,
    PRIMARY KEY (dog_id, track_id),
    FOREIGN KEY (dog_id)
        REFERENCES dog(dog_id),
    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
);

CREATE TABLE std_time (
    track_id INT,
    grade VARCHAR(32),
    std_time FLOAT,
    std_sect_time FLOAT,
    PRIMARY KEY (track_id, grade),
    FOREIGN KEY (track_id) 
        REFERENCES track(track_id)
);