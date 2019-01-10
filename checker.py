import requests
import telegram
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


# http status ex)404, 500
ERROR_CHECK_CODE = ['4', '5']

# telegram bot token
TELEGRAM_BOT_TOKEN_KEY = '742478084:AAHh3xU_RfPV29T4DK_0M3h5T55F5fnmBsU'

# telegram channel
TELEGRAM_CHAT = '@bima_status'

# site url
SITE_URL = 'https://www.bima.kr'


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def checker():
    target_site_url = SITE_URL
    status_recive_channel = TELEGRAM_CHAT
    now_tz_seoul = datetime.utcnow() + timedelta(seconds=32400)
    try:
        website = requests.get(target_site_url)
        website_status_code = str(website.status_code)
        if website_status_code[0] in ERROR_CHECK_CODE:
            status_message = '%s status code is %s. \n%s\nstatus check time is %s' \
                             % (target_site_url, website_status_code, website.reason,
                                now_tz_seoul.strftime("%Y-%m-%d %H:%M:%S"))
            send_message(status_message, TELEGRAM_BOT_TOKEN_KEY, status_recive_channel)
        else:
            return 'site status all green'
    except Exception:
        status_message = '%s site connect refused. now %s' % (target_site_url, now_tz_seoul.strftime("%Y-%m-%d %H:%M:%S"))
        send_message(status_message, TELEGRAM_BOT_TOKEN_KEY, status_recive_channel)


def send_message(message, token, chat_id):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


sched.start()
