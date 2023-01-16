import results_storer_mysql as rsm
from datetime import datetime

a = datetime(2020, 2, 29)

rsm.store_race_results(60, a)

# have not gone through january 2021