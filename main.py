from config import (
    CHECKIN_TIME,
    SLACK_LINK,
    SLACK_EMAIL,
    SLACK_PASSWORD,
    COACH,
    CANVAS_LINK,
    CANVAS_EMAIL,
    CANVAS_PASSWORD,
    GECKODRIVER,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as options_f
from selenium.webdriver.chrome.options import Options as options_c
from selenium.webdriver.common.keys import Keys
from termcolor import colored, cprint
from selenium import webdriver
from time import sleep
from os import system, path
import datetime
import pyfiglet

from core.slack_bot import Bot
from core.canvas_bot import Bot_activities
from core.input_handler import Input_handler
from core.time_handler import Time_handler

CLEAR = lambda: system("clear")
PATH = path.realpath(__file__)
PATH = PATH.replace("core/main.py", f"gecko/{GECKODRIVER}")
PATH = PATH.replace("core\main.py", f"gecko\{GECKODRIVER}")


def bot_cicle():
    print("Check-in Time!")
    print("------------------")
    print("Getting activity for the check-in...")
    bot_activities = Bot_activities()
    canvas_activity = bot_activities.get_activities()
    print("------------------")
    print(f"Activity for the day: {canvas_activity}")
    print("------------------")
    print("Sending message to check-in thread...")
    bot = Bot()
    bot.login_slack(SLACK_LINK)
    bot.find_thread(canvas_activity, "Tudo ok")

    Time_handler.terminal_countdown()
    sleep(1800)


def main():
    coach = False

    if COACH != "":
        coach = Input_handler.coach_verify()
    if coach:
        coach_time = Input_handler.coach_time()

    time_left = input("Countdown for check-in time? (y/n) ")

    while True:

        sleep(1)
        CLEAR()

        if time_left.lower() == "y":
            if coach:
                Time_handler.time_left(coach, coach_time)
            else:
                Time_handler.time_left()

        if coach:
            if (
                coach_time
                < datetime.datetime.now().strftime("%H:%M:%S")
                < coach_time.replace("0", "1", 2)
            ):
                print("Coach check-in Time!")
                bot = Bot()
                bot.login_slack(COACH)
                bot.find_thread()

            if (
                CHECKIN_TIME["MORNING"]["start"]
                < datetime.datetime.now().strftime("%H:%M:%S")
                < CHECKIN_TIME["MORNING"]["end"]
                or CHECKIN_TIME["EVENING"]["start"]
                < datetime.datetime.now().strftime("%H:%M:%S")
                < CHECKIN_TIME["EVENING"]["end"]
            ):
                bot_cicle()

        else:
            if (
                CHECKIN_TIME["MORNING"]["start"]
                < datetime.datetime.now().strftime("%H:%M:%S")
                < CHECKIN_TIME["MORNING"]["end"]
                or CHECKIN_TIME["EVENING"]["start"]
                < datetime.datetime.now().strftime("%H:%M:%S")
                < CHECKIN_TIME["EVENING"]["end"]
            ):
                bot_cicle()


if __name__ == "__main__":
    main()
