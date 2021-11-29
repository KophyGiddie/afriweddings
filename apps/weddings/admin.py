from django.contrib import admin
from apps.weddings.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(Wedding)
admin.site.register(WeddingTeam)
admin.site.register(WeddingRole)
admin.site.register(WeddingMedia)
admin.site.register(WeddingFAQ)
admin.site.register(WeddingScheduleEvent)
admin.site.register(WeddingSchedule)
