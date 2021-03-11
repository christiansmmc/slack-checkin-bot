from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from os import system
import pyfiglet
from termcolor import colored, cprint

#AQUI A URL DO CANAL qX-coaches, ONDE OCORRE O CHECK-IN PARA OS COACHES.
COACH = "https://app.slack.com/client/TQZR39SET/G01767VRLSG"

#AQUI A URL DO CANAL DO SEU FACILITADOR, ONDE OCORRE O CHECK-IN.
DEV = "https://app.slack.com/client/TQZR39SET/G018D3ASP88"

#AQUI O PATH DO PERFIL DO FIREFOX
FIREFOX_PROFILE = "../../../.mozilla/firefox/thc4d1aq.default-release"

#AQUI O HORARIO DO CHECK-IN
CHECKIN_TIME = {"MORNING": {"start":"09:00:15", "end": "09:05:00"},
                "EVENING": {"start": "14:00:15", "end": "14:05:00"}}

CLEAR = lambda: system('clear')

class Bot:
    def __init__(self):

        fp = webdriver.FirefoxProfile(FIREFOX_PROFILE)

        self.driver = webdriver.Firefox(fp)

    @staticmethod
    def is_coach():
        slack_bot = pyfiglet.figlet_format('SLACK BOT', font="banner3")
        colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
        print(colored_slack_bot)
        coach = input('Você é coach? (y/n) :')

        if coach.lower() == "y":
            return True

        if coach.lower() == "n":
            return False

    @staticmethod
    def coach_time():
        print('--------------')
        checkin_time = input('Horario do check-in: (11/13) : ')
        horario = f'{checkin_time}:00:00'
        return horario

    @staticmethod
    def student_questions():
        print('--------------')
        checkin_time_doing = input('O que esta fazendo: ')
        checkin_time_doubts = input('Dificuldades: ')
        return checkin_time_doing, checkin_time_doubts,

    @staticmethod
    def calculate_time(s2):
        s1 = datetime.datetime.now().strftime('%H:%M:%S')
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)
        segundos = tdelta.seconds
        tempo = str(datetime.timedelta(seconds=segundos))
        final = tempo.split(":")
        return final[0], final[1], final[2],

    @staticmethod
    def time_left(is_coach = False, coach_time = ""):
        slack_bot = pyfiglet.figlet_format('SLACK BOT', font="banner3")
        if is_coach: 
            if 9 < int(datetime.datetime.now().strftime("%H")) < int(coach_time.split(":")[0]):
                hours, minutes, seconds = Bot.calculate_time(coach_time)
                timer = pyfiglet.figlet_format(f'{hours} : {minutes} : {seconds}', font="banner3")
                colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
                print()
                print(colored_slack_bot)
                print(f'Tempo para o próximo checkin: \n{timer}')

            elif int(coach_time.split(":")[0]) < int(datetime.datetime.now().strftime("%H")) < 14:
                hours, minutes, seconds = Bot.calculate_time(CHECKIN_TIME["EVENING"]["start"])
                timer = pyfiglet.figlet_format(f'{hours} : {minutes} : {seconds}', font="banner3")
                colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
                print()
                print(colored_slack_bot)
                print(f'Tempo para o próximo checkin: \n{timer}')

            else:
                hours, minutes, seconds = Bot.calculate_time(CHECKIN_TIME["MORNING"]["start"])
                timer = pyfiglet.figlet_format(f'{hours} : {minutes} : {seconds}', font="banner3")
                colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
                print()
                print(colored_slack_bot)
                print(f'Tempo para o próximo checkin: \n{timer}')        

        elif not is_coach:    
            if 9 < int(datetime.datetime.now().strftime("%H")) < 14:
                hours, minutes, seconds = Bot.calculate_time(CHECKIN_TIME["EVENING"]["start"])
                timer = pyfiglet.figlet_format(f'{hours} : {minutes} : {seconds}', font="banner3")
                colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
                print()
                print(colored_slack_bot)
                print(f'Tempo para o próximo checkin: \n{timer}')

            else:
                hours, minutes, seconds = Bot.calculate_time(CHECKIN_TIME["MORNING"]["start"])
                timer = pyfiglet.figlet_format(f'{hours} : {minutes} : {seconds}', font="banner3")
                colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
                print()
                print(colored_slack_bot)
                print(f'Tempo para o próximo checkin: \n{timer}')

    def write_checkin(self, text1, text2):
        input_to_write = self.driver.find_element_by_css_selector(
            "div .p-threads_footer__input.p-message_input .p-message_input_field .ql-editor"
        )

        if text1 != "":
            What_im_doing = f'1. {text1.capitalize()}'
            problems = text2.capitalize()
            input_to_write.send_keys(What_im_doing + Keys.CONTROL + Keys.ENTER)
            input_to_write.send_keys(problems)
            input_to_write.send_keys(Keys.ENTER)

        if text1 == "":
            input_to_write.send_keys("Check-in")
            input_to_write.send_keys(Keys.ENTER)

        CLEAR()
        slack_bot = pyfiglet.figlet_format('SLACK BOT', font="banner3")
        colored_slack_bot = colored(slack_bot, 'red', 'on_white', attrs=['reverse', 'dark'])
        print()
        print(colored_slack_bot)
        print("Check-in feito!\nTRAVA DE SEGURANÇA ATIVADA PRA EVITAR VÁRIOS CHECKINS, DENTRO DE 30 MINS SEU TIMER VOLTARÁ")

    def search(self, link: str, text1: str = "", text2: str = ""):

        self.driver.get(link)

        sleep(2)

        last_child = self.driver.find_element_by_css_selector(
            ".c-virtual_list__scroll_container > .c-virtual_list__item:last-child[role=listitem]")

        if "Devs check-in" in last_child.text or "Coaches check-in" in last_child.text:

            hover = ActionChains(self.driver).move_to_element(last_child)
            hover.perform()

            thread_button = self.driver.find_element_by_css_selector(".c-message_actions__button:nth-child(2)")

            thread_button.click()

            sleep(2)

            self.write_checkin(text1, text2)

            sleep(1)
            
            self.driver.close()

            sleep(1800)
            
        else:
            CLEAR()

            print("Check-in não encontrado\nTentando novamente em 20 segundos...")

            self.driver.close()

            sleep(20)

def main():

    is_coach = Bot.is_coach()
    if is_coach:
        coach_time = Bot.coach_time()

    doing, doubts = Bot.student_questions()

    print('--------------')
    time_left = input('Gostaria de um countdown: (y/n)')

    while True:
        
        sleep(1)
        CLEAR()
        
        if time_left.lower() == "y":
            if is_coach:
                Bot.time_left(is_coach, coach_time)
            else:
                Bot.time_left()

        if is_coach:
            if (
                    coach_time < datetime.datetime.now().strftime("%H:%M:%S") < coach_time.replace("0", "1", 2)
            ):
                print("Coach check-in Time!")
                bot = Bot()
                bot.search(COACH)
            if (
                    CHECKIN_TIME["MORNING"]["start"] < datetime.datetime.now().strftime("%H:%M:%S") < CHECKIN_TIME["MORNING"]["end"]
                    or CHECKIN_TIME["EVENING"]["start"] < datetime.datetime.now().strftime("%H:%M:%S") < CHECKIN_TIME["EVENING"]["end"]
            ):
                print("Check-in Time!")
                bot = Bot()
                bot.search(DEV, doing, doubts)
                
        else:
            if (
                    CHECKIN_TIME["MORNING"]["start"] < datetime.datetime.now().strftime("%H:%M:%S") < CHECKIN_TIME["MORNING"]["end"]
                    or CHECKIN_TIME["EVENING"]["start"] < datetime.datetime.now().strftime("%H:%M:%S") < CHECKIN_TIME["EVENING"]["end"]
            ):
                print("Check-in Time!")
                bot = Bot()
                bot.search(DEV, doing, doubts)

if __name__ == "__main__":
    main()
