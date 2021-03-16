from environs import Env

env = Env()
env.read_env()

#SLACK
COACH = env('COACH')

DEV = env('SLACK_DEV_URL')

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


#CANVAS
CANVAS_LINK = env('CANVAS_LINK')
CANVAS_EMAIL = env('CANVAS_EMAIL')
CANVAS_PASSWORD = env('CANVAS_PASSWORD')

#SELENIUM
GECKODRIVER = env('GECKODRIVER')