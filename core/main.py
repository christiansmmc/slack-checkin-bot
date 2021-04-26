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

CLEAR = lambda: system("clear")
PATH = path.realpath(__file__)
PATH = PATH.replace("core/main.py", f"gecko/{GECKODRIVER}")
PATH = PATH.replace("core\main.py", f"gecko\{GECKODRIVER}")


class Bot:
    def __init__(self):
        # FIREFOX DRIVER
        # options = options_f()
        # options.headless = True
        # self.driver = webdriver.Firefox(executable_path=PATH, options=options)

        # CHROME DRIVER
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
                int(CHECKIN_TIME["EVENING"]["start"][0:2])
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

        if (
            datetime.datetime.now().strftime("%H")
            == CHECKIN_TIME["EVENING"]["start"][0:2]
        ):

            if CHECKIN_TIME["EVENING"]["start"][0:2] in slack_checkin_to_send[0].text:
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


class Input_handler:
    @staticmethod
    def coach_verify():
        slack_bot = pyfiglet.figlet_format("SLACK BOT", font="banner3")
        colored_slack_bot = colored(
            slack_bot, "red", "on_white", attrs=["reverse", "dark"]
        )
        print(colored_slack_bot)
        coach = input("Você é coach? (y/n) :")

        if coach.lower() == "y":
            return True

        if coach.lower() == "n":
            return False

    @staticmethod
    def coach_time():
        print("--------------")
        checkin_time = input("Horario do check-in: (11/13) : ")
        horario = f"{checkin_time}:00:00"
        return horario

    @staticmethod
    def student_questions():
        print("--------------")
        checkin_time_doing = input("O que esta fazendo: ")
        checkin_time_doubts = input("Dificuldades: ")
        return (
            checkin_time_doing,
            checkin_time_doubts,
        )


class Time_handler:
    @staticmethod
    def time_calculator(time):
        s1 = datetime.datetime.now().strftime("%H:%M:%S")
        fmt = "%H:%M:%S"
        tdelta = datetime.datetime.strptime(time, fmt) - datetime.datetime.strptime(
            s1, fmt
        )
        segundos = tdelta.seconds
        tempo = str(datetime.timedelta(seconds=segundos))
        final = tempo.split(":")
        return (
            final[0],
            final[1],
            final[2],
        )

    @staticmethod
    def terminal_countdown(
        hours=0,
        minutes=0,
        seconds=0,
        show_timer=False,
        message="Tempo para o próximo checkin:",
    ):
        slack_bot = pyfiglet.figlet_format("SLACK BOT", font="banner3")
        timer = pyfiglet.figlet_format(f"{hours}:{minutes}:{seconds}", font="banner3")
        colored_slack_bot = colored(
            slack_bot, "red", "on_white", attrs=["reverse", "dark"]
        )
        print()
        print(colored_slack_bot)
        print(f"{message}\n{timer}") if show_timer else print(
            "Check-in feito!\nTRAVA DE SEGURANÇA ATIVADA PRA EVITAR VÁRIOS CHECK-INS\nDENTRO DE 30 MINS SEU TIMER VOLTARÁ"
        )

    @staticmethod
    def time_left(coach=False, coach_time=""):

        if coach:
            if (
                9
                <= int(datetime.datetime.now().strftime("%H"))
                < int(coach_time.split(":")[0])
            ):
                hours, minutes, seconds = Time_handler.time_calculator(coach_time)
                Time_handler.terminal_countdown(hours, minutes, seconds, True)

            elif (
                int(coach_time.split(":")[0])
                <= int(datetime.datetime.now().strftime("%H"))
                < 14
            ):
                hours, minutes, seconds = Time_handler.time_calculator(
                    CHECKIN_TIME["EVENING"]["start"]
                )
                Time_handler.terminal_countdown(hours, minutes, seconds, True)

            else:
                hours, minutes, seconds = Time_handler.time_calculator(
                    CHECKIN_TIME["MORNING"]["start"]
                )
                Time_handler.terminal_countdown(hours, minutes, seconds, True)

        elif not coach:
            if 9 <= int(datetime.datetime.now().strftime("%H")) < 14:
                hours, minutes, seconds = Time_handler.time_calculator(
                    CHECKIN_TIME["EVENING"]["start"]
                )
                Time_handler.terminal_countdown(hours, minutes, seconds, True)

            else:
                hours, minutes, seconds = Time_handler.time_calculator(
                    CHECKIN_TIME["MORNING"]["start"]
                )
                Time_handler.terminal_countdown(hours, minutes, seconds, True)


class Bot_activities:
    def __init__(self):
        # FIREFOX DRIVER
        # options = options_f()
        # options.headless = True
        # self.driver = webdriver.Firefox(executable_path=PATH, options=options)

        # CHROME DRIVER
        chrome_options = options_c()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
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
            doing = for_today[0].split("\n")[0]

        close_tabs = self.driver.find_elements_by_class_name("icon-mini-arrow-down")
        close_tabs.reverse()

        for tab in close_tabs:
            if tab.is_displayed():
                tab.click()
                sleep(0.2)

        return doing


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
