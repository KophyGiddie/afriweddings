from django.contrib import admin
from apps.checklists.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(ChecklistCategory)
admin.site.register(ChecklistSchedule)
admin.site.register(Checklist)
