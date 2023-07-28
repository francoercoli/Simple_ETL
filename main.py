import pandas as pd
from connection import get_token
from ETL.extract import extract
from ETL.transform import transform
from ETL.load import load


# 0 - Connection with Spotify - Authorization and Access Token
token = get_token()

# 1 - Extract Data
data = extract(token)

# 2 - Transofrm Data
song_df = transform(data)

# 3 - Load Data
load(song_df)
