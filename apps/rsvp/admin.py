from django.contrib import admin
from apps.rsvp.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(RSVPQuestion)
admin.site.register(RSVP)
admin.site.register(RSVPAnswer)
