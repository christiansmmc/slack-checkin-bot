from config import (
    CHECKIN_TIME,
    SLACK_EMAIL,
    SLACK_PASSWORD,
    COACH,
    GECKODRIVER,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as options_c
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from os import system, path
import datetime

CLEAR = lambda: system("clear")
PATH = path.realpath(__file__)
PATH = PATH.replace("core/slack_bot.py", f"gecko/{GECKODRIVER}")
PATH = PATH.replace("core\slack_bot.py", f"gecko\{GECKODRIVER}")


class Bot:
    def __init__(self):
        # CHROME DRIVER OPTIONS
        chrome_options = options_c()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(PATH, options=chrome_options)

    def write_checkin(self, text1, text2):
        input_to_write = self.driver.find_element_by_css_selector(
            "div .p-threads_footer__input.p-message_input .p-message_input_field .ql-editor"
        )

        if text1 != "":
            what_im_doing = f"1. {text1.capitalize()}"
            problems = text2.capitalize()
            input_to_write.send_keys(what_im_doing + Keys.CONTROL + Keys.ENTER)
            input_to_write.send_keys(problems)
            input_to_write.send_keys(Keys.ENTER)

        if text1 == "":
            input_to_write.send_keys("Check-in")
            input_to_write.send_keys(Keys.ENTER)

        CLEAR()

    def login_slack(self, link):

        self.driver.get(link)

        sleep(2)

        workspace_link = self.driver.find_element_by_xpath('//*[@id="domain"]')

        workspace_link.send_keys("kenzieacademybrasil")

        workspace_button = self.driver.find_element_by_xpath(
            "/html/body/main/div/div/div/div/div[2]/form/button"
        )
        workspace_button.click()

        sleep(2)

        slack_email = self.driver.find_element_by_xpath('//*[@id="email"]')
        slack_email.send_keys(SLACK_EMAIL)
        slack_password = self.driver.find_element_by_xpath('//*[@id="password"]')
        slack_password.send_keys(SLACK_PASSWORD)

        login_button = self.driver.find_element_by_xpath('//*[@id="signin_btn"]')
        login_button.click()

        sleep(2)

    def find_thread(self, text1="", text2=""):

        slack_messages = self.driver.find_elements_by_css_selector(
            ".c-message_kit__gutter"
        )

        slack_checkin_to_send = [
            message
            for message in slack_messages
            if "Devs check-in" in message.text or "Coaches check-in" in message.text
        ]

        slack_checkin_to_send.reverse()

        if (
            datetime.datetime.now().strftime("%H")
            == CHECKIN_TIME["MORNING"]["start"][0:2]
        ):

            if (
                CHECKIN_TIME["MORNING"]["start"][0:2].lstrip("0")
                in slack_checkin_to_send[0].text
            ):

                hover = ActionChains(self.driver).move_to_element(
                    slack_checkin_to_send[0]
                )
                hover.perform()

                thread_button = self.driver.find_element_by_css_selector(
                    ".c-message_actions__button:nth-child(2)"
                )

                thread_button.click()

                sleep(2)

                self.write_checkin(text1, text2)

                sleep(1)

                # silence thread notifications
                hover = ActionChains(self.driver).move_to_element(
                    slack_checkin_to_send[0]
                )
                hover.perform()
                option_button = self.driver.find_element_by_css_selector(
                    ".c-message_actions__button:last-child"
                )
                option_button.click()
                silence_button = self.driver.find_element_by_css_selector(
                    ".c-menu__items > div:first-child"
                )
                silence_button.click()

        elif (
            datetime.datetime.now().strftime("%H")
            == CHECKIN_TIME["EVENING"]["start"][0:2]
        ):

            if (
                CHECKIN_TIME["EVENING"]["start"][0:2].lstrip("0")
                in slack_checkin_to_send[0].text
            ):
                hover = ActionChains(self.driver).move_to_element(
                    slack_checkin_to_send[0]
                )
                hover.perform()

                thread_button = self.driver.find_element_by_css_selector(
                    ".c-message_actions__button:nth-child(2)"
                )

                thread_button.click()

                sleep(2)

                self.write_checkin(text1, text2)

                sleep(1)

                # silence thread notifications
                hover = ActionChains(self.driver).move_to_element(
                    slack_checkin_to_send[0]
                )
                hover.perform()
                option_button = self.driver.find_element_by_css_selector(
                    ".c-message_actions__button:last-child"
                )
                option_button.click()
                silence_button = self.driver.find_element_by_css_selector(
                    ".c-menu__items > div:first-child"
                )
                silence_button.click()

        else:
            CLEAR()

            print("Check-in não encontrado\nTentando novamente em 20 segundos...")

            sleep(20)
