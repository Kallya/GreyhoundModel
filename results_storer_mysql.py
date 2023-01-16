import mysql.connector
import results_scraper as rs
import betfair_price_scraper as bps
from datetime import datetime, timedelta

last_id_select = "SELECT LAST_INSERT_ID()"
track_insert_check = "SELECT track_id FROM track WHERE location = %s AND distance = %s"
track_insert = "INSERT INTO track(location, distance) VALUES(%s, %s)"
race_insert = """INSERT INTO race_record
    (date, track_id, grade, race_no, runner_num)
    VALUES(%s, %s, %s, %s, %s)"""
dog_insert = "INSERT IGNORE INTO dog(dog_id) VALUES(%s)"
dog_result_insert = """INSERT INTO dog_race_result
    (race_id, dog_id, box, place, time, sect_time, weight, bsp)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

# retrieves day_num worth of consecutive days
# of results until last_date (datetime)
def store_race_results(day_num, last_date: datetime):
    # setup db connection
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="passwd",
        database="race_data"
    )
    cursor = database.cursor()

    result_links = rs.get_result_links(day_num, last_date)
    for date in result_links:
        # bsp mostly in day after
        bsp_data = bps.get_price_data(date+timedelta(1))
        for link in result_links[date]:
            race_results = rs.get_race_results(link)
            for race in race_results:
                # insert new track if not exists
                track_vals = (race["track_loc"], race["distance"])
                cursor.execute(track_insert_check, track_vals)
                row = cursor.fetchone()
                if row == None:
                    cursor.execute(track_insert, track_vals)
                    cursor.execute(last_id_select)
                    track_id = cursor.fetchone()[0]
                else:
                    track_id = row[0]

                # insert race record
                race_vals = (
                        date.strftime("%Y-%m-%d"), 
                        track_id, 
                        race["grade"], 
                        race["race_no"],
                        race["runner_num"]
                        )
                cursor.execute(race_insert, race_vals)
                cursor.execute(last_id_select)
                race_id = cursor.fetchone()[0]

                # insert dog and its result data for race
                for row in race["results"]:
                    cursor.execute(dog_insert, (row["dog_id"],))
                    strp_id = row["dog_id"].replace("'", '')
                    try:
                        bsp = float(bps.find_races(bsp_data, dog_id=strp_id)["bsp"])
                    except:
                        bsp = None
                        
                    result_vals = (
                        race_id,
                        row["dog_id"],
                        row["box"],
                        row["place"],
                        row["time"],
                        row["sect_time"],
                        row["weight"],
                        bsp
                    )
                    cursor.execute(dog_result_insert, result_vals)
            
    database.commit()
    database.close()