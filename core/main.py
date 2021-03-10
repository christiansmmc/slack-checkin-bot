from time import sleep
import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


COACH_Q2 = "https://app.slack.com/client/TQZR39SET/G01767VRLSG"
ALUNO_Q3 = "https://app.slack.com/client/TQZR39SET/G018D3ASP88"

class Bot:
    def __init__(self):

        fp = webdriver.FirefoxProfile("../../.mozilla/firefox/thc4d1aq.default-release")

        self.driver = webdriver.Firefox(fp)

    @staticmethod
    def is_coach():
        print('--------------')
        coach = input('Você é coach? (y/n) :')

        if coach == "y":
            print(coach)
            return True

        if coach == "n":
            print(coach)
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


    def search(self, link:str, text1: str = "", text2:str = ""):
        print(f'->{text1}<-->{text2}<-')

        self.driver.get(link)
        
        sleep(2)

        last_child = self.driver.find_element_by_css_selector(
            ".c-virtual_list__scroll_container > .c-virtual_list__item:last-child[role=listitem]"
        )

        if "Devs check-in" in last_child.text or "Coaches check-in" in last_child.text:

            hover = ActionChains(self.driver).move_to_element(last_child)
            hover.perform()

            thread_button = self.driver.find_element_by_css_selector(
                ".c-message_actions__button:nth-child(2)"
            )

            thread_button.click()

            sleep(2)

            input_to_write = self.driver.find_element_by_css_selector(
                ".p-threads_footer__input.p-message_input .p-message_input_field .ql-editor"
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

            print("Check-in feito!")
            sleep(1800)



is_coach = Bot.is_coach()
if is_coach:
    coach_time = Bot.coach_time()

doing, doubts = Bot.student_questions()




while True:
    sleep(1)
    
    hours = int(datetime.datetime.now().strftime("%H"))
    minutes = int(datetime.datetime.now().strftime("%M"))
    seconds = int(datetime.datetime.now().strftime("%S"))
    
    if 9 < int(datetime.datetime.now().strftime("%H")) < 14:
        print(f'Faltam {abs(hours - 14)} horas e {abs(minutes - 60)} minutos e {abs(seconds - 60)} segundos')
    else: 
        print(f'Faltam {abs(hours - 9)} horas e {abs(minutes - 60)} minutos e {abs(seconds - 60)} segundos')

    if is_coach:
        if (
        coach_time < datetime.datetime.now().strftime("%H:%M:%S") < coach_time.replace("0", "1", 2) 
        ):   
            print("Coach check-in Time!")
            bot = Bot()
            bot.search(COACH_Q2)
        if (
            "09:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "09:05:00"
            or "14:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "14:05:00"
        ):   
            print("Check-in Time!")
            bot = Bot()
            bot.search(ALUNO_Q3, doing, doubts)
    
    else: 
        
       if (
            "09:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "09:05:00"
            or "14:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "14:05:00"
        ):   
        print("Check-in Time!")
        bot = Bot()
        bot.search(ALUNO_Q3, doing, doubts)
        


