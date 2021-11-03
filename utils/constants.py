from datetime import datetime

TODAY = datetime.now()
TODAY_PATH = TODAY.strftime("%Y/%m/%d/%H/%M/%S")
PROFILE_PIC_DIR = 'PROFILE/' + TODAY_PATH + '/'
WALLPOST_PIC_DIR = 'WALLPOST/' + TODAY_PATH + '/'
