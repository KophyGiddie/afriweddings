from django.contrib import admin
from apps.budget.models import *

"""
Register your models here to appear in Admin Backend

"""
admin.site.register(BudgetCategory)
admin.site.register(BudgetExpense)
admin.site.register(ExpensePayment)
