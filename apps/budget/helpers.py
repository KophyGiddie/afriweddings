from django.db.models import Sum
from apps.weddings.models import Wedding
from decimal import Decimal, InvalidOperation
from apps.budget.models import BudgetCategory, ExpensePayment, BudgetExpense
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
        myvalue = Decimal(value)
        return myvalue
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


def get_expense_payment(id):
    try:
        return ExpensePayment.objects.get(id=id)
    except (ExpensePayment.DoesNotExist, ValidationError):
        return None


def update_expense(myexpense):
    total_paid = myexpense.payments.filter(is_paid=True).aggregate(Sum('payment_amount'))['payment_amount__sum']

    if total_paid is None or total_paid == 'None':
        total_paid = Decimal(0)

    myexpense.paid = total_paid
    myexpense.save()


def get_budget_expense_by_name(name, mycategory):
    try:
        BudgetExpense.objects.get(name=name, category=mycategory)
        return True
    except BudgetCategory.DoesNotExist:
        return None


def get_budget_category_by_name(name, wedding):
    try:
        BudgetCategory.objects.get(name=name, wedding=wedding)
        return True
    except BudgetCategory.DoesNotExist:
        return None


def create_budget_category(name, mywedding, currency, myuser):
    mycategory = BudgetCategory.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  total_estimated_cost=Decimal(0),
                                  total_final_cost=Decimal(0),
                                  total_paid=Decimal(0),
                                  total_pending=Decimal(0),
                                  currency=currency,
                                  created_by=myuser
                                )
    return mycategory
