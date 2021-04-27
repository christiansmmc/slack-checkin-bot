from config import CHECKIN_TIME

from termcolor import colored, cprint
import datetime
import pyfiglet


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
