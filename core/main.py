from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

## MODIFY
COACH = "https://app.slack.com/client/TQZR39SET/G01767VRLSG"
DEV = "https://app.slack.com/client/TQZR39SET/G018D3ASP88"
FIREFOX_PROFILE = "../../../.mozilla/firefox/thc4d1aq.default-release"
##

class Bot:
    def __init__(self):

        fp = webdriver.FirefoxProfile(FIREFOX_PROFILE)

        self.driver = webdriver.Firefox(fp)

    @staticmethod
    def is_coach():
        print('--------------')
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
        if is_coach and 9 < int(datetime.datetime.now().strftime("%H")) < int(coach_time.split(":")[0]):
            hours, minutes, seconds = Bot.calculate_time(coach_time)
            print(f'Faltam {hours} horas e {minutes} minutos e {seconds} segundos')

        elif 14 < int(datetime.datetime.now().strftime("%H")) < 9:
            hours, minutes, seconds = Bot.calculate_time('09:00:16')
            print(f'Faltam {hours} horas e {minutes} minutos e {seconds} segundos')        

        elif is_coach and int(coach_time.split(":")[0]) < int(datetime.datetime.now().strftime("%H")) < 14:
            hours, minutes, seconds = Bot.calculate_time('14:00:16')
            print(f'Faltam {hours} horas e {minutes} minutos e {seconds} segundos')

        elif not is_coach:    
            if 9 < int(datetime.datetime.now().strftime("%H")) < 14:
                hours, minutes, seconds = Bot.calculate_time('14:00:16')
                print(f'Faltam {hours} horas e {minutes} minutos e {seconds} segundos')

            elif 14 < int(datetime.datetime.now().strftime("%H")) < 9:
                hours, minutes, seconds = Bot.calculate_time('09:00:16')
                print(f'Faltam {hours} horas e {minutes} minutos e {seconds} segundos')

    def write_checkin(self, text1, text2):
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
            
            self.driver.close()

            sleep(1800)


        else:
            print("Check-in não encontrado")

def main():

    is_coach = Bot.is_coach()
    if is_coach:
        coach_time = Bot.coach_time()

    doing, doubts = Bot.student_questions()

    print('--------------')
    time_left = input('Gostaria de um countdown: (y/n)')

    while True:

        sleep(1)
        
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
                    "09:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "09:05:00"
                    or "14:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "14:05:00"
            ):
                print("Check-in Time!")
                bot = Bot()
                bot.search(DEV, doing, doubts)
                
        else:
            if (
                    "09:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "09:05:00"
                    or "14:00:15" < datetime.datetime.now().strftime("%H:%M:%S") < "14:05:00"
            ):
                print("Check-in Time!")
                bot = Bot()
                bot.search(DEV, doing, doubts)

if __name__ == "__main__":
    main()