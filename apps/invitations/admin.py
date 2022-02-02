from django.contrib import admin
from apps.invitations.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(Invitation)
admin.site.register(BetaInvitation)
