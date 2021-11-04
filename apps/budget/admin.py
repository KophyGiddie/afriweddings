from django.contrib import admin
from apps.budget.models import *

# Register your models here.
admin.site.register(BudgetCategory)
admin.site.register(BudgetExpense)

