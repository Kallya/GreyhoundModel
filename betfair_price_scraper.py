import pandas as pd
from datetime import datetime

allowed_locs = ["AUS", "NZL"]
base_price_url = "https://promo.betfair.com/betfairsp/prices/dwbfgreyhoundwin"
price_data_path = "bsp_data/"

def get_name(selection_name):
    return selection_name[3:].upper()

def get_price_data(date: datetime):
    d_str = date.strftime("%d-%m-%Y")
    url = base_price_url + d_str.replace('-', '') + ".csv"
    
    return get_cleaned_data(url)

# data cleaning from csv file
def get_cleaned_data(csv_url) -> pd.DataFrame:
    df = pd.read_csv(csv_url, on_bad_lines="warn")
    df = df.iloc[:, :8]

    # isolate only AUS and NZL races
    for t in enumerate(df.loc[:, "MENU_HINT"]):
        try:
            location = t[1].split(' / ')[0]
            if location not in allowed_locs:
                df.drop(t[0], inplace=True)
        except:
            df.drop(t[0], inplace=True)

    # remove unnecessary columns
    df.drop(columns=[
        "EVENT_ID", 
        "MENU_HINT",
        "EVENT_NAME",
        "SELECTION_ID", 
        "WIN_LOSE",
        "EVENT_DT",
        ], inplace=True)

    df.rename(columns={
        "SELECTION_NAME": "dog_id",
        "BSP": "bsp"
    }, inplace=True)

    # transform data to make more meaningful
    df["dog_id"] = df["dog_id"].apply(get_name)

    return df

# retrieve price file from betfair directory and format
# dates is list of datetimes
def get_price_files(dates):
    for d in dates:
        d_str = d.strftime("%d-%m-%Y")
        url = base_price_url + d_str.replace('-', '') + ".csv"
        with open(price_data_path+d_str+".csv", 'w') as f:
            f.write(get_cleaned_data(url).to_csv(index_label=False))

# search for races by filters
def find_races(cleaned_df: pd.DataFrame, dog_id=None, bsp_filter=None):
    query = []
    if dog_id != None:
        query.append("dog_id == @dog_id")
    if bsp_filter != None:
        query.append("bsp " + bsp_filter)
        
    return cleaned_df.query(" and ".join(query))