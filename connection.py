from requests import post
import json
import base64
from selenium import webdriver
import time
from urllib.parse import urlparse, parse_qs, urlencode


CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
username = "username"

def authorization():
    redirect_url = "https://localhost:8080"
    authorization_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "scope": "user-read-recently-played",
        "response_type": "code",
        "redirect_uri": redirect_url
    }
    url = authorization_url + "?" + urlencode(params)

    driver = webdriver.Chrome()  
    driver.get(url)
    
    print("You have 10 seconds to login in your Spotify account")
    time.sleep(10)

    code_url = driver.current_url

    parsed_url = urlparse(code_url)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get('code')
    if code:
        code = code[0]
    driver.quit()
    return code

def get_token():
    code = authorization()
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    myheaders = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    mydata = {"grant_type":"authorization_code","code":code,"redirect_uri":"https://localhost:8080"}

    result = post(url, headers=myheaders, data=mydata)

    json_result = json.loads(result.content)
    if result.status_code == 200 :
        token = json_result["access_token"]
    else:
        print("Error"+str(result.status_code))
        token = None
    return token
