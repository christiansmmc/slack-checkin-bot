from environs import Env

env = Env()
env.read_env()

#SLACK
CHECKIN_TIME = {
    "MORNING": {
        "start": env('CHECKIN_TIME_AM_INITIAL'),
        "end": env('CHECKIN_TIME_AM_FINAL')
        },
    "EVENING": {
        "start": env('CHECKIN_TIME_PM_INITIAL'),
        "end": env('CHECKIN_TIME_PM_FINAL')
        }
    }

COACH = env('COACH')
SLACK_LINK = env('SLACK_LINK')
SLACK_EMAIL = env('SLACK_EMAIL')
SLACK_PASSWORD = env('SLACK_PASSWORD')

#CANVAS
CANVAS_LINK = env('CANVAS_LINK')
CANVAS_EMAIL = env('CANVAS_EMAIL')
CANVAS_PASSWORD = env('CANVAS_PASSWORD')

#SELENIUM
GECKODRIVER = env('GECKODRIVER')