import mysql.connector
import base64
import results_scraper

database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=base64.b64decode("WWFzdW8xMjM=").decode("utf-8"),
    database="greyhound_data"
)

cursor = database.cursor()

# setup database
# scrape data from bsp records
# fill database
# functions to calculate features for model
# train model
# test/validate model
# test profitability
# reflect/revise and repeat

database.close()