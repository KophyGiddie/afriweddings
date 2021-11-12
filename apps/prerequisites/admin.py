from django.contrib import admin
from apps.prerequisites.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(DefaultChecklistCategory)
admin.site.register(DefaultChecklistSchedule)
admin.site.register(DefaultChecklist)
admin.site.register(DefaultWeddingRole)
admin.site.register(Country)
