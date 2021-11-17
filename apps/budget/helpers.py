from django.db.models import Sum
from apps.weddings.models import Wedding
from decimal import Decimal, InvalidOperation
from apps.budget.models import BudgetCategory, ExpensePayment, BudgetExpense
from django.core.exceptions import ValidationError


def update_budget_category(mybudget):
    """
    Updates budget category after a new expense is added

    """
    total_final_cost = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']
    total_estimated_cost = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']
    total_paid = mybudget.budget_expense.all().aggregate(Sum('final_cost'))['final_cost__sum']

    if total_final_cost is None or total_final_cost == 'None':
        total_final_cost = Decimal(0)

    if total_estimated_cost is None or total_estimated_cost == 'None':
        total_estimated_cost = Decimal(0)

    if total_paid is None or total_paid == 'None':
        total_paid = Decimal(0)

    total_pending = total_final_cost - total_paid
    mybudget.total_final_cost = total_final_cost
    mybudget.total_estimated_cost = total_estimated_cost
    mybudget.total_paid = total_paid
    mybudget.total_pending = total_pending
    mybudget.save()


def validate_decimal(value):
    """
    Validates any number field if it is a valid decimal

    """
    try:
        myvalue = Decimal(value)
        return myvalue
    except InvalidOperation:
        return False


def get_currency(request):
    """
    Returns the currency as set when creating the wedding

    """
    mywedding = Wedding.objects.get(id=request.user.wedding_id)
    return mywedding.currency


def get_budget_category(id):
    """
    Returns budget category using the primary key

    """
    try:
        return BudgetCategory.objects.get(id=id)
    except (BudgetCategory.DoesNotExist, ValidationError):
        return None


def get_expense_payment(id):
    """
    Returns expense payment using the primary key

    """
    try:
        return ExpensePayment.objects.get(id=id)
    except (ExpensePayment.DoesNotExist, ValidationError):
        return None


def update_expense(myexpense):
    """
    Update expenses total_paid when a payment is made

    """
    total_paid = myexpense.payments.filter(is_paid=True).aggregate(Sum('payment_amount'))['payment_amount__sum']

    if total_paid is None or total_paid == 'None':
        total_paid = Decimal(0)

    final_cost = myexpense.final_cost
    pending = final_cost - total_paid

    myexpense.paid = total_paid
    myexpense.pending = pending
    myexpense.save()


def get_budget_expense_by_name(name, mycategory):
    """
    Returns budget expense using the name

    """
    try:
        BudgetExpense.objects.get(name=name, category=mycategory)
        return True
    except BudgetExpense.DoesNotExist:
        return None


def get_budget_category_by_name(name, wedding):
    """
    Returns budget category using the name

    """
    try:
        BudgetCategory.objects.get(name=name, wedding=wedding)
        return True
    except BudgetCategory.DoesNotExist:
        return None


def create_budget_category(name, mywedding, currency, myuser):
    """
    Creates a budget category with the parameters supplied

    """
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


def create_budget_expense(name, mycategory, currency, estimated_cost, final_cost, myuser):
    """
    Creates a budget expense with the parameters supplied

    """
    myexpense = BudgetExpense.objects.create(
        name=name,
        category=mycategory,
        currency=currency,
        estimated_cost=Decimal(estimated_cost),
        final_cost=Decimal(final_cost),
        paid=Decimal(0),
        pending=Decimal(0),
        created_by=myuser
    )
    return myexpense


def create_expense_payment(payment_date, payment_due, paid_by, myexpense, currency, is_paid, payment_amount, payment_method, myuser):
    """
    Creates an expense payment

    """
    mypayment = ExpensePayment.objects.create(
        payment_date=payment_date,
        payment_due=payment_due,
        paid_by=paid_by,
        expense=myexpense,
        currency=currency,
        is_paid=is_paid,
        payment_amount=Decimal(payment_amount),
        payment_method=payment_method,
        created_by=myuser
    )
    return mypayment

