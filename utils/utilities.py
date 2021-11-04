import os
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from random import randrange
from utils import sendgrid
from django.template.loader import render_to_string
from utils.bulk_create_manager import BulkCreateManager
from apps.checklists.models import Checklist, ChecklistCategory, ChecklistSchedule


def generate_new_token():
    CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwwxyz'
    LENGTH = 9
    new_code = ''
    for i in range(LENGTH):
        new_code += CHARSET[randrange(0, len(CHARSET))]
    return new_code


def hash_string(mystring):
    hasher = PBKDF2PasswordHasher()
    hashed = hasher.encode(password=mystring, salt=os.environ.get('PASS_SALT'), iterations=24000).split('24000')[1]
    return hashed


def send_activation_email(myuser, token, title):
    context = {
        'user': myuser,
        'token': token,
    }
    msg_html = render_to_string('email_templates/activation_email.html', context)
    sendgrid.send_email(title, msg_html, os.environ.get('FROM_EMAIL'), myuser.email)


def send_forgot_password_email(myuser, token, title):
    context = {
        'user': myuser,
        'token': token,
    }
    msg_html = render_to_string('email_templates/forgot_password.html', context)
    sendgrid.send_email(title, msg_html, os.environ.get('FROM_EMAIL'), myuser.email)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def bulk_create_items(queryset):
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for row in queryset:
        bulk_mgr.add(Checklist(attr1=row['attr1'], attr2=row['attr2']))
    bulk_mgr.done()
