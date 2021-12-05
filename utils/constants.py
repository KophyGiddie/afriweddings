from datetime import datetime
import os
from utils.utilities import generate_image_upload_prefix

TODAY = datetime.now()
TODAY_PATH = TODAY.strftime("%Y/%m/%d/%H/%M/%S")
PROFILE_PIC_DIR = 'PROFILE/' + TODAY_PATH + generate_image_upload_prefix() + '/'
WALLPOST_PIC_DIR = 'WALLPOST/' + TODAY_PATH + generate_image_upload_prefix() + '/'

if "LIVE" in os.environ:
    WEB_APP_URL = 'https://afriweddingsweb.herokuapp.com/'
else:
    WEB_APP_URL = 'https://afriweddingsweb.herokuapp.com/'


# DEFAULT ROLES
BRIDE = "Bride"
GROOM = "Groom"
BUSINESS = "Business"
RELATIVE = "Relative"


# INVITATION TYPES
WEDDING_PARTNER = "Partner"
WEDDING_TEAM = "Team"
WEDDING_GUEST = "Guest"
