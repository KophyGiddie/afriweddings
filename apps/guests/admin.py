from django.contrib import admin
from apps.guests.models import *

# Register your models here.
admin.site.register(Guest)
admin.site.register(GuestEvent)
admin.site.register(GuestGroup)
