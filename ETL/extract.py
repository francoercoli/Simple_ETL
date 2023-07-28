import requests
import datetime


def extract(token):
    return get_recently_played(token)

def get_recently_played(authorization_token):
    # Return a JSON with recently played tracks.
    myheaders = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Authorization":"Bearer {token}".format(token=authorization_token)
    }
    today = get_date()
    today_unix_timestamp = int(today.timestamp())*1000
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=today_unix_timestamp), headers = myheaders)
    if r.status_code == 200:
        pass
    else:
        print(r.text)
    return r.json()

def get_date():
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return today
