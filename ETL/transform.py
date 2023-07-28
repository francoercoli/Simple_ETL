import pandas as pd
from ETL.extract import get_date
from dateutil import parser
import datetime


def transform(data):
    song_df = pd.DataFrame(get_dict(data))
    if check_if_valid_data(song_df):
        print("Data valid, proceed to load stage.")
    return song_df
    
def get_dict(data):
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["artists"][0]["name"])
        date_arg = utc_zone(song["played_at"])
        played_at_list.append(date_arg)
        timestamps.append(date_arg[0:10])
    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    return song_dict

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty: #Check if dataframe is empty
        print("No songs downloaded. Finishing execution.")
        return False
    
    if pd.Series(df["played_at"]).is_unique: #Primary key check
        pass
    else:
        raise Exception("Primary Key Check is violated.")
    
    if df.isnull().values.any(): #Check for nulls
        raise Exception("Null valued found.")
    
    today = get_date()
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:     #Check that all timestamps are of today´s date
        if datetime.datetime.strptime(timestamp,"%Y-%m-%d") != today:
            raise Exception("At least one of the returned song is not from today.")

    return True

def utc_zone(date):
    date= parser.isoparse(date[:-1])
    dif = datetime.timedelta(hours=3)
    date_arg = date - dif
    return str(date_arg)