from datetime import datetime
import os

TODAY = datetime.now()
TODAY_PATH = TODAY.strftime("%Y/%m/%d/%H/%M/%S")
PROFILE_PIC_DIR = 'PROFILE/' + TODAY_PATH + '/'
WALLPOST_PIC_DIR = 'WALLPOST/' + TODAY_PATH + '/'

if "LIVE" in os.environ:
    WEB_APP_URL = 'https://afriweddingsweb.herokuapp.com/'
else:
    WEB_APP_URL = 'https://afriweddingsweb.herokuapp.com/'


#DEFAULT ROLES
BRIDE = "Bride"
GROOM = "Groom"
BUSINESS = "Business"
RELATIVE = "Relative"


# INVITATION TYPES
WEDDING_PARTNER = "Partner"
WEDDING_TEAM = "Team"
WEDDING_GUEST = "Guest"
