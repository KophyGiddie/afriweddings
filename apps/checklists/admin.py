from django.contrib import admin
from apps.checklists.models import *

# Register your models here.
admin.site.register(ChecklistCategory)
admin.site.register(ChecklistSchedule)
admin.site.register(Checklist)
