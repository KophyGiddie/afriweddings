from django.db.models import Sum
from apps.weddings.models import Wedding
from decimal import Decimal, InvalidOperation
from apps.budget.models import BudgetCategory
from django.core.exceptions import ValidationError


def update_budget_category(mybudget):
    total_final_cost = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']
    total_estimated_cost = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']
    total_paid = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']

    if total_final_cost is None or total_final_cost == 'None':
        total_final_cost = Decimal(0)

    if total_estimated_cost is None or total_estimated_cost == 'None':
        total_estimated_cost = Decimal(0)

    if total_paid is None or total_paid == 'None':
        total_paid = Decimal(0)

    mybudget.total_final_cost = total_final_cost
    mybudget.total_estimated_cost = total_estimated_cost
    mybudget.total_paid = total_paid
    mybudget.save()


def validate_decimal(value):
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


def get_currency(request):
    mywedding = Wedding.objects.get(id=request.user.wedding_id)
    return mywedding.currency


def get_budget_category(id):
    try:
        return BudgetCategory.objects.get(id=id)
    except (BudgetCategory.DoesNotExist, ValidationError):
        return None


def update_expense(myexpense):
    total_paid = myexpense.payments.filter(is_paid=True).aggregate(Sum('payment_amount'))['payment_amount__sum']

    if total_paid is None or total_paid == 'None':
        total_paid = Decimal(0)

    myexpense.paid = total_paid
    myexpense.save()
