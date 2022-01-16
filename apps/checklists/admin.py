from django.contrib import admin
from apps.checklists.models import *


class ChecklistScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')


admin.site.register(ChecklistCategory)
admin.site.register(ChecklistSchedule, ChecklistScheduleAdmin)
admin.site.register(Checklist)
