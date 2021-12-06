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
admin.site.register(DefaultFAQ)
admin.site.register(DefaultRSVPQuestion)
admin.site.register(DefaultBudgetExpense)
admin.site.register(DefaultBudgetCategory)
admin.site.register(DefaultBudget)
