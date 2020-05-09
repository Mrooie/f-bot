import datetime as dt
from decouple import config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
import time

FLAG = True
BUFFER_DAYS = 3
MONTHS = {
    "sty": "01",
    "lut": "02",
    "mar": "03",
    "kwi": "04",
    "maj": "05",
    "cze": "06",
    "lip": "07",
    "sie": "08",
    "wrz": "09",
    "paź": "10",
    "lis": "11",
    "gru": "12",
}

# Install chromedriver on MacOs with: brew cask install chromedriver
chromedriver = r"/usr/local/bin/chromedriver"
browser = webdriver.Chrome(executable_path=chromedriver)

# Open Frisco page
browser.get("https:frisco.pl")

# Wait for popup (needs to be modified if Frisco changes popup window in the future with class-name change)
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, "fixed-popup-wrapper"))
    WebDriverWait(browser, 10).until(element_present)

    # Close the popup
    close_el = browser.find_element_by_class_name("fixed-popup-wrapper").click()
except NoSuchElementException:
    pass

# Login
browser.find_element_by_link_text("Zaloguj się").click()

# Wait until login popup shows or throw an exception
element_present = EC.presence_of_element_located((By.NAME, "username"))
WebDriverWait(browser, 10).until(element_present)

# Fill the login deets and hit enter :)
browser.find_element_by_name("username").send_keys(config("EMAIL"))
password = browser.find_element_by_name("password")
password.send_keys(config("PASSWORD"))
password.send_keys(Keys.ENTER)

while FLAG:
    # Wait until delivery date loads
    time.sleep(10)
    element_present = EC.presence_of_element_located((By.XPATH, "//*[@id='header']/div/div[1]/div/div[4]/div/div[2]"))
    WebDriverWait(browser, 10).until(element_present)

    delivery_deets = browser.find_element_by_xpath("//*[@id='header']/div/div[1]/div/div[4]/div/div[2]").text

    delivery_date = delivery_deets.split(" ")

    reservations = browser.find_element_by_xpath("//*[@id='header']/div/div[1]/div/div[4]")

    # If delivery is open for tomorrow
    if delivery_date[0] == "jutro":
        # Open reservations panel
        reservations.click()

        # Wait until reservations tool loads
        element_present = EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]"))
        WebDriverWait(browser, 10).until(element_present)

        # Open reservations
        element_present = EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]"))
        WebDriverWait(browser, 10).until(element_present)

        browser.find_element_by_xpath("//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]").click()

        browser.find_element_by_class_name("available").click()
        browser.find_element_by_xpath("//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/div[2]").click()
        time.sleep(10)

        # If reservation is accepted
        if browser.find_element_by_xpath("//*[@id='header']/div/div[1]/div/div[4]/div/div[1]").text == "Twoja rezerwacja":
            FLAG = False
            break

        # If reservation failed due to any error, reload page and try again.
        else:
            browser.refresh()

    else:
        date_now = dt.date.today()

        # If current mont has higher number then reservation month, it means, that reservation is made for next year.
        deli_month = MONTHS[delivery_date[1]]
        if int(date_now.month) > int(deli_month):
            year_to_check = date_now.year + 1
        else:
            year_to_check = date_now.year

        # Construct a date of reservation with proper year, that is not included on a page
        date_to_check = f"{year_to_check}-{MONTHS[delivery_date[1]]}-{delivery_date[0]}"

        # Create the latest reservation date that you accept. Use BUFFER_DAYS to set the value of days ahead date_now.
        end_date = dt.datetime.strptime(date_now.strftime("%d/%m/%Y"), "%d/%m/%Y") + dt.timedelta(days=BUFFER_DAYS)

        date_to_check = dt.datetime.strptime(date_to_check, "%Y-%m-%d")

        if end_date >= date_to_check:
            # Open reservations panel
            reservations.click()

            # Wait until reservations tool loads
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]"))
            WebDriverWait(browser, 10).until(element_present)

            # Open reservations
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]"))
            WebDriverWait(browser, 10).until(element_present)

            browser.find_element_by_xpath("//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]").click()

            browser.find_element_by_class_name("available").click()
            browser.find_element_by_xpath(
                "//*[@id='wrapper']/span/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/div[2]").click()
            time.sleep(10)

            # If reservation is accepted
            if browser.find_element_by_xpath(
                    "//*[@id='header']/div/div[1]/div/div[4]/div/div[1]").text == "Twoja rezerwacja":
                FLAG = False
                break

            # If reservation failed due to any error, reload page and try again.
            else:
                browser.refresh()

        else:
            browser.refresh()
