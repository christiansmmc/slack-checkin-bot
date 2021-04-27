from termcolor import colored, cprint
import pyfiglet


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
