from datetime import datetime, timedelta
import mysql.connector

target_record_table = "race_record_temp"
target_result_table = "dog_race_result_temp"
target_track_table = "track"

get_race_date = f"SELECT date FROM {target_record_table} WHERE race_id = %s"
get_race_track = f"SELECT track_id FROM {target_record_table} WHERE race_id = %s"

# args (race_id, dog_id)
q_get_overall_win_rate = f"""SELECT COUNT(IF(b.place = 1, 1, NULL)) / COUNT(*)
    FROM (
        SELECT race_id FROM {target_record_table} 
        WHERE date < ({get_race_date})
    ) a
    INNER JOIN {target_result_table} b
    ON b.race_id = a.race_id AND b.dog_id = %s"""

# args (race_id, dog_id)
q_get_time_since_last_start = f"""SELECT DATEDIFF(({get_race_date}), a.date) 
    FROM (
        SELECT race_id, date FROM {target_record_table} 
        WHERE date < ({get_race_date})
    ) a
    RIGHT JOIN {target_result_table} b
    ON b.race_id = a.race_id AND b.dog_id = %s
    ORDER BY date DESC
    LIMIT 1"""

# args (race_id, dog_id, race_id)
q_get_track_win_rate = f"""SELECT COUNT(IF(b.place = 1, 1, NULL)) / COUNT(*)
    FROM (
        SELECT race_id, track_id FROM {target_record_table} 
        WHERE date < ({get_race_date})
    ) a
    INNER JOIN {target_result_table} b
    ON b.dog_id = %s AND b.race_id = a.race_id 
    AND a.track_id = ({get_race_track})"""

# args (race_id, dog_id, n_races)
q_get_recent_weight_stddev = f"""SELECT STDDEV(b.weight) 
    FROM (
        SELECT race_id, date FROM {target_record_table} 
        WHERE date < ({get_race_date})
    ) a
    INNER JOIN {target_result_table} b 
    ON b.dog_id = %s AND b.race_id = a.race_id
    ORDER BY date DESC
    LIMIT %s"""

# args (race_id, dog_id, race_id)
q_get_track_total_starts = f"""SELECT COUNT(*)
    FROM (
        SELECT race_id, track_id FROM {target_record_table} 
        WHERE date < ({get_race_date})
    ) a
    INNER JOIN {target_result_table} b
    ON b.dog_id = %s AND b.race_id = a.race_id 
    AND a.track_id = ({get_race_track})"""





# differentiate between no exp vs no wins?
# cursor is the sql cursor
# how to deal with missing data? (ie. when there is no race history
# cause first race or database does not contain data that far back)

def get_sql_result(query, cursor, null_val, conv_func, *args):
    cursor.execute(query, args)
    result = cursor.fetchone()[0]

    if result == None:
        return null_val
    
    return conv_func(result)

def get_overall_win_rate(cursor, race_id, dog_id):
    return get_sql_result(
        q_get_overall_win_rate,
        cursor,
        0,
        float,
        race_id,
        dog_id
    )

def get_time_since_last_start(cursor, race_id, dog_id):
    return get_sql_result(
        q_get_time_since_last_start,
        cursor,
        365,
        int,
        race_id,
        race_id,
        dog_id
    )

def get_track_win_rate(cursor, race_id, dog_id):
    return get_sql_result(
        q_get_track_win_rate,
        cursor,
        0,
        float,
        race_id,
        dog_id,
        race_id
    )

def get_recent_weight_stddev(cursor, race_id, dog_id, n):
    return get_sql_result(
        q_get_recent_weight_stddev,
        cursor,
        0,
        float,
        race_id,
        dog_id,
        race_id,
        n
    )

def get_track_total_starts(cursor, race_id, dog_id):
    return get_sql_result(
        q_get_track_total_starts,
        cursor,
        0,
        int,
        race_id,
        dog_id,
        race_id
    )


    
if __name__ == "__main__":
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="passwd",
        database="race_data"
    )
    cursor = database.cursor()

    get_time_since_last_start(22231, "AARON ALPACA", cursor)

    database.close()
