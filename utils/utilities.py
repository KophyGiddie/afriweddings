import os
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from random import randrange
from utils import sendgrid
from utils.constants import WEB_APP_URL
from django.template.loader import render_to_string
from apps.weddings.models import Wedding
from dateutil.parser._parser import ParserError
from dateutil.parser import parse
from django.core.exceptions import ValidationError


def get_admin_wedding(wedding_id, request):
    is_admin = False
    try:
        mywedding = Wedding.objects.get(id=wedding_id)

        if mywedding.author == request.user:
            is_admin = True

        if request.user in mywedding.admins.all():
            is_admin = True

        if is_admin:
            return mywedding

        return None
    except Wedding.DoesNotExist:
        return None


def get_wedding(request):
    try:
        mywedding = Wedding.objects.get(id=request.user.wedding_id)
        return mywedding
    except (Wedding.DoesNotExist, ValidationError):
        return None


def generate_invitation_code():
    CHARSET = '0123456789BCDFGHJKLMNPQRSTbcdfghjklmnpqrstvw-'
    LENGTH = 32
    new_code = ''
    for i in range(LENGTH):
        new_code += CHARSET[randrange(0, len(CHARSET))]
    return new_code


def hash_string(mystring):
    hasher = PBKDF2PasswordHasher()
    hashed = hasher.encode(password=mystring, salt=os.environ.get('PASS_SALT'), iterations=24000).split('24000')[1]
    return hashed


def send_invitation_email(myinvitation, first_name):
    title = 'Afriweddings Invitations'
    context = {
        'title': title,
        'first_name': first_name,
        'first_name': myinvitation.invited_by.first_name,
        'user_role': myinvitation.invitee_role.role,
        'button_url': '%saccept-invite/%s' % (WEB_APP_URL, myinvitation.invitation_code)
    }
    msg_html = render_to_string('email_templates/invitation_email.html', context)
    sendgrid.send_email(title, msg_html, os.environ.get('FROM_EMAIL'), myinvitation.email)


def send_activation_email(myuser, token, title):
    context = {
        'title': title,
        'user': myuser,
        'button_url': '%sverify-account/%s' % (WEB_APP_URL, token)
    }
    msg_html = render_to_string('email_templates/activation_email.html', context)
    sendgrid.send_email(title, msg_html, os.environ.get('FROM_EMAIL'), myuser.email)


def send_forgot_password_email(myuser, token, title):
    context = {
        'title': title,
        'user': myuser,
        'button_url': '%sconfirm-password/%s' % (WEB_APP_URL, token)
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


def validate_date(date):
    try:
        mydate = parse(date)
        return mydate
    except ParserError:
        return None
