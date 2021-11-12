from django.contrib import admin
from apps.seating.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(SeatingTable)
admin.site.register(SeatingChart)
