from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import logging
from getpass import getpass
import time
import sys
import glob
import os

def get_next_sunday():
    d = datetime.date.today()
    while d.weekday() != 6:
        d += datetime.timedelta(1)
    return_date = d.strftime("%a, %b %d")
    return_date.replace("0","")

    return return_date

def find_meetup_event(meetup_username, meetup_pw, headless, attempts):
    #config options
    #ind chromedriver
    driver_file = glob.glob('chrome*')[0]
    cwd = os.getcwd()
    chrome_driver_location = os.path.join(cwd, driver_file)

    ##set up chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_driver_location, options=chrome_options)
    driver.implicitly_wait(1)

    ##begin navigation
    driver.get(r'https://www.meetup.com')
    log_in_btn = driver.find_element_by_xpath('//span[text()="Log in"]').click()
    email_submit = driver.find_element_by_xpath('//input[@id="email"]').send_keys(meetup_username)
    pw_submit = driver.find_element_by_xpath('//input[@id="password"]').send_keys(meetup_pw)
    submit_creds_btn = driver.find_element_by_xpath('//input[@id="loginFormSubmit"]').click()

    driver.get(r'https://www.meetup.com/Alexandria-Indoor-Volleyball/')
    #search_date = get_next_sunday()
    search_date = 'Mon, Mar 21'
    upcoming_events = driver.find_elements_by_xpath('//div[@class="chunk"]')
    rsvp_success = False

    logger.info("Checking posted events...")
    for event in upcoming_events:
        if rsvp_success == True:
            break
        else:
            try:
                event_date = event.find_element_by_xpath('.//span[text()=\'{}\']'.format(search_date))
                event.click()
                attend_btn = driver.find_element_by_xpath('//button[@class="gtmEventFooter--attend-btn"]').click()
                rsvp_success = True
                logger.info("RSVP'd! You're good to go.")
                driver.close()
                sys.exit()
            except Exception as e:
                None
    logger.info("Event not found, retrying in 30 seconds. Attempts: "+str(attempts))
    driver.close()


def main(meetup_username, meetup_pw, headless, end_time):
    attempts = 1
    while time.time() < end_time:
        find_meetup_event(meetup_username, meetup_pw, headless, attempts)
        time.sleep(30)
        attempts+=1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    meetup_username = input("Meetup Email Address: ")
    meetup_pw = getpass("Password: ")
    while True:
        headless = input("Run Headless? (y/n): ")
        if headless == 'y':
            headless = True
            break
        elif headless == 'n':
            headless = False
            break
        else:
            print("y or n dingus")
    hours = input("Hours to Monitor: ")
    end_time = time.time() + (int(hours)*360)

    logger.info("Starting Scraper...")
    main(meetup_username, meetup_pw, headless, end_time)
