from config import (
    CANVAS_LINK,
    CANVAS_EMAIL,
    CANVAS_PASSWORD,
    GECKODRIVER,
)
from selenium.webdriver.chrome.options import Options as options_c
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from os import system, path
import random
import datetime

CLEAR = lambda: system("clear")
PATH = path.realpath(__file__)
PATH = PATH.replace("core/canvas_bot.py", f"gecko/{GECKODRIVER}")
PATH = PATH.replace("core\canvas_bot.py", f"gecko\{GECKODRIVER}")


class Bot_activities:
    def __init__(self):
        # CHROME DRIVER OPTIONS
        chrome_options = options_c()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--lang=en")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(PATH, options=chrome_options)

    def get_activities(self):

        dt = datetime.datetime.today()
        mydate = datetime.datetime.now()

        TODAY = dt.day
        MONTH = mydate.strftime("%b")

        self.driver.get(CANVAS_LINK)
        email = self.driver.find_element_by_xpath(
            '//*[@id="pseudonym_session_unique_id"]'
        )
        email.send_keys(CANVAS_EMAIL)

        password = self.driver.find_element_by_xpath(
            '//*[@id="pseudonym_session_password"]'
        )
        password.send_keys(CANVAS_PASSWORD)
        password.send_keys(Keys.ENTER)

        sleep(2)

        open_tabs = self.driver.find_elements_by_class_name("collapsed_module")
        open_tabs.reverse()

        for tab in open_tabs:
            tab.click()
            sleep(0.2)

        sleep(1)

        all_sprints = self.driver.find_elements_by_class_name("ig-info")
        for_today = [
            activity.text
            for activity in all_sprints
            if f"{MONTH} {TODAY}" in activity.text
        ]

        if len(for_today) == 0:
            doing = "Revendo conceitos"
        else:
            random.shuffle(for_today)
            doing = for_today[0].split("\n")[0]

        close_tabs = self.driver.find_elements_by_class_name("icon-mini-arrow-down")
        close_tabs.reverse()

        for tab in close_tabs:
            if tab.is_displayed():
                tab.click()
                sleep(0.2)

        return doing
