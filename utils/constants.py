from datetime import datetime
import os
from random import randrange


def generate_image_upload_prefix():
    CHARSET = '0123456789BCDFGHJKLMNPQRSTbcdfghjklmnpqrstvw'
    LENGTH = 16
    new_code = ''
    for i in range(LENGTH):
        new_code += CHARSET[randrange(0, len(CHARSET))]
    return new_code


TODAY = datetime.now()
TODAY_PATH = TODAY.strftime("%Y/%m/%d/%H/%M/%S")
PROFILE_PIC_DIR = 'PROFILE/' + TODAY_PATH + generate_image_upload_prefix() + '/'
WALLPOST_PIC_DIR = 'WALLPOST/' + TODAY_PATH + generate_image_upload_prefix() + '/'

if "LIVE" in os.environ:
    WEB_APP_URL = 'https://www.afriweddings.com/'
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
