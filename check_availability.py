import os
import time

import dill as pickle
import browser_cookie3
from requests_html import HTMLSession
import smtplib


def save_cookies(output_path):
    cookies = browser_cookie3.chrome(domain_name=".amazon.com")
    with open(output_path, "wb") as f:
        pickle.dump(cookies, f)


def check_availability(url, cookies_path):
    with open(cookies_path, "rb") as f:
        cookies = pickle.load(f)

    session = HTMLSession()
    while True:
        r = session.get(url, verify=False, cookies=cookies)
        if "Delivery available" in r.html.html:
            print("Delivery available!!!")

            sender_email = "pikadue@gmail.com"
            receiver_email = "diihuu@umich.edu"
            password = input("Type your password and press enter: ")
            message = "Whole Foods delivery is available!"

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

            break
        else:
            print("Not available, sleeping for an hour...")
            time.sleep(3600)


if __name__ == "__main__":
    cookies_path = "cookies_amazon.pkl"

    # only need to run once, to extract amazon's cookies from your local Chrome and pickle it
    if not os.path.exists(cookies_path):
        save_cookies(cookies_path)

    # it can be run in any server without Chrome
    check_availability(
        url='https://www.amazon.com/alm/storefront?almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=nav_cs_whole_foods_in_region',
        cookies_path=cookies_path,
    )
