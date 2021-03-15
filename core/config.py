from environs import Env

env = Env()
env.read_env()

#AQUI A URL DO CANAL qX-coaches, ONDE OCORRE O CHECK-IN PARA OS COACHES.
COACH = env('COACH')

#AQUI A URL DO CANAL DO SEU FACILITADOR, ONDE OCORRE O CHECK-IN.
DEV = env('SLACK_DEV_URL')

#AQUI O PATH DO PERFIL DO FIREFOX
FIREFOX_PROFILE = env('FIREFOX_PROFILE')

#AQUI O HORARIO DO CHECK-IN
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