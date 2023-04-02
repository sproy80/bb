from asyncio.windows_events import NULL
from concurrent.futures import thread
from hashlib import new
from lib2to3.pgen2 import driver
import webbrowser
from xml.dom.minidom import Element
from fyers_api import fyersModel
from fyers_api import accessToken
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import autoit as ait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from urllib.parse import parse_qs
import pyotp


import os
import time
import json


# //Global varriables

os.environ["PATH"] += os.pathsep + r"C:\selenium_webdrivers"

totp = "ECQIME6KJDCZUKN7UJYF2CEDE7AEPPR7"
pin = "7861"
app_id = "B5ZFYFYM0W-100"
secret_key = "MA7YGV5Y67"
redirect_uri = "http://127.0.0.1:8080/login"
response_type = "code"
grant_type = "authorization_code"
state = "abcdefg"
scope = ""
nonce = ""


# wbdriver.maximize_window()
# wbdriver.get(url="www.google.com")
# wbdriver.implicitly_wait(5)


def login():
    access_token = ""
    print("started...")
    if not os.path.exists("access_token.txt"):

        access_token = get_access_token(auth_code=get_auth_code())
    else:
        print('Exist')
        with open("access_token.txt", "r") as f:
            access_token = f.read()
    return access_token


def get_auth_code():
    wbdriver = webdriver.Chrome()
    session = accessToken.SessionModel(client_id=app_id,
                                       secret_key=secret_key, redirect_uri=redirect_uri,
                                       response_type=response_type, grant_type=grant_type)

    authUri = session.generate_authcode()
    # webbrowser.open(authUri, new=1)
    print(authUri)
    wbdriver.get(url=authUri)
    wbdriver.implicitly_wait(2)

    # Check if Login required

    if wbdriver.find_element(By.ID, 'fy_client_id') != NULL:
        print("Login Required")
        # Send UserID
        wbdriver.find_element(By.ID, 'fy_client_id').send_keys('XS08767')
        # Click on Submit Button
        wbdriver.find_element(By.ID, 'clientIdSubmit').click()

        # TOTP page will appear
        time.sleep(3)

        otp = pyotp.TOTP(totp).now()

        print(otp)

        wbdriver.find_element(By.ID, 'first').send_keys(otp[0])
        wbdriver.find_element(By.ID, 'second').send_keys(otp[1])
        wbdriver.find_element(By.ID, 'third').send_keys(otp[2])
        wbdriver.find_element(By.ID, 'fourth').send_keys(otp[3])
        wbdriver.find_element(By.ID, 'fifth').send_keys(otp[4])
        wbdriver.find_element(By.ID, 'sixth').send_keys(otp[5])

        time.sleep(1)

        wbdriver.find_element(By.ID, 'confirmOtpSubmit').click()

        # Password page will appear
        # WebDriverWait(wbdriver, 5).until(
        #     EC.element_to_be_clickable((By.ID, "fy_client_pwd"))
        # )
        time.sleep(3)
        # Send Password
        # print("1")
        # wbdriver.find_element(By.ID, 'fy_client_pwd').click()
        # print("2")
        # wbdriver.find_element(By.ID, 'fy_client_pwd').send_keys("Sanjay@1811")
        # print("3")
        # # Click on Submit Button
        # wbdriver.find_element(By.ID, 'loginSubmit').click()

        # PIN page will appear
        ele = wbdriver.find_element(By.ID, 'first')
        # ele.click()
        act = ActionChains(wbdriver)
        # act.click(on_element=ele)
        # PIN page will appear

        # act.send_keys(Keys.TAB)
        # act.send_keys(Keys.TAB)
        # act.send_keys("7861")
        # act.perform()
        # ait.win_get_handle("FYERS - Your gateway to investing")
        ait.win_activate("FYERS - Your gateway to investing")
        ait.send("7")
        ait.send("8")
        ait.send("6")
        ait.send("1")
        wbdriver.implicitly_wait(2)
        # Click on Submit Button
        wbdriver.find_element(By.ID, 'verifyPinSubmit').click()
    else:
        print("Login not required")


# Redirect URL need to collect
    WebDriverWait(wbdriver, 20).until(
        EC.staleness_of(ele)
    )
    page_url = wbdriver.current_url
    print('Auth URL : ' + page_url)

    parsed_url = urlparse(page_url)
    auth_code = parse_qs(parsed_url.query)['auth_code'][0]

    print("Auth Code : " + auth_code)
    return auth_code


def get_access_token(auth_code):

    session = accessToken.SessionModel(client_id=app_id,
                                       secret_key=secret_key, redirect_uri=redirect_uri,
                                       response_type=response_type, grant_type=grant_type)

    session.set_token(auth_code)

    response = session.generate_token()

    data = json.dumps(response)

    data = json.loads(data)
    access_token = data["access_token"]

    with open("access_token.txt", "w") as f:
        print(access_token)
        f.write(str(access_token))

    return access_token


# print(login())
