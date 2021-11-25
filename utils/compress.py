from io import StringIO
from PIL import Image as mypil
import PIL
from boto.s3.connection import S3Connection
import os

AWS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = 'afriweddings-static'


def start_compressing(theimage):
    conn = S3Connection(AWS_KEY, AWS_SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)

    pic = bucket.get_key(theimage)

    try:
        if pic.size > 100000:
            input_file = StringIO(pic.get_contents_as_string())

            img = mypil.open(input_file)

            basewidth = 800

            wpercent = (basewidth / float(img.size[0]))

            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

            tmp = StringIO()
            img.save(tmp, 'JPEG', optimize=True, quality=85)
            tmp.seek(0)

            output_data = tmp.getvalue()

            headers = dict()
            headers['Content-Type'] = 'image/jpeg'
            headers['Content-Length'] = str(len(output_data))
            pic.set_contents_from_string(output_data, headers=headers, policy='public-read')

            tmp.close()
            input_file.close()
            print ('compression done v1')
            return True
        return 'File Size Less than 100KB'
    except:
        return 'Unable to do Compression'