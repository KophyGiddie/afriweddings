from datetime import datetime
import os

TODAY = datetime.now()
TODAY_PATH = TODAY.strftime("%Y/%m/%d/%H/%M/%S")
PROFILE_PIC_DIR = 'PROFILE/' + TODAY_PATH + '/'
WALLPOST_PIC_DIR = 'WALLPOST/' + TODAY_PATH + '/'

if "LIVE" in os.environ:
    WEB_APP_URL = 'https://afriweddings.netlify.app/'
else:
    WEB_APP_URL = 'https://afriweddings.netlify.app/'
