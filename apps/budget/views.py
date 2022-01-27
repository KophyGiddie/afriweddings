from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.budget.serializer import BudgetCategorySerializer, BudgetExpenseSerializer, ExpensePaymentSerializer, ExtendedExpensePaymentSerializer
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding, validate_date
from apps.budget.helpers import (
    update_expense, update_budget_category, get_currency,
    validate_decimal, get_budget_category, get_expense_payment,
    get_budget_category_by_name, get_budget_expense_by_name,
    create_budget_category, create_budget_expense, create_expense_payment
)
from decimal import Decimal
from apps.budget.models import BudgetCategory, BudgetExpense, ExpensePayment


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    model = BudgetCategory
    serializer_class = BudgetCategorySerializer
    queryset = BudgetCategory.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created budget categories

        """
        myqueryset = BudgetCategory.objects.filter(wedding__id=request.user.wedding_id)
        serializer = BudgetCategorySerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a budget category

        """
        name = request.data.get('name', None)

        if not name:
            return Response(error_response("Please provide the name value", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)
        existing_category = get_budget_category_by_name(name, mywedding)

        if existing_category:
            return Response(error_response("A category with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        mycategory = create_budget_category(name, mywedding, get_currency(request), request.user)

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        edits a budget category

        """
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        mycategory.save()

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_expenses')
    def get_expenses(self, request, *args, **kwargs):
        """
        returns a list of expenses of a single category whose pk is passed in the URL

        """
        mycategory = self.get_object()
        myqueryset = mycategory.budget_expense.select_related('category').all()
        serializer = BudgetExpenseSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a budget category

        """
        mycategory = self.get_object()
        if mycategory.created_by == request.user:
            mycategory.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class BudgetExpenseViewSet(viewsets.ModelViewSet):
    model = BudgetExpense
    serializer_class = BudgetExpenseSerializer
    queryset = BudgetExpense.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created budget expenses

        """
        myqueryset = BudgetExpense.objects.select_related('category').filter(category__wedding__id=request.user.wedding_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = self.get_serializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        creates a budget expense and updates budget category with the details of the expense

        """
        name = request.data.get('name', None)
        category_id = request.data.get('category_id', None)
        currency = get_currency(request)
        estimated_cost = request.data.get('estimated_cost', 0)
        final_cost = request.data.get('final_cost', 0)

        if not name:
            return Response(error_response("Please provide the name value", '141'), status=HTTP_400_BAD_REQUEST)

        if not category_id:
            return Response(error_response("Please provide a category", '142'), status=HTTP_400_BAD_REQUEST)

        myresults = validate_decimal(final_cost)
        if not myresults:
            return Response(error_response("Invalid Final Cost", '143'), status=HTTP_400_BAD_REQUEST)

        myresults = validate_decimal(estimated_cost)
        if not myresults:
            return Response(error_response("Invalid Estimated cost", '144'), status=HTTP_400_BAD_REQUEST)

        mycategory = get_budget_category(category_id)
        if not mycategory:
            return Response(error_response("Invalid Budget Category", '149'), status=HTTP_400_BAD_REQUEST)

        existing_category = get_budget_expense_by_name(name, mycategory)

        if existing_category:
            return Response(error_response("An expense with this name already exist for this category", '139'), status=HTTP_400_BAD_REQUEST)

        myexpense = create_budget_expense(name, mycategory, currency, estimated_cost, final_cost, request.user)

        # update total values of budget category
        update_budget_category(mycategory)

        serializer = BudgetExpenseSerializer(myexpense, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Edits a budget a expense

        """
        myexpense = self.get_object()

        if request.data.get('estimated_cost') and request.data.get('estimated_cost') != '':
            myexpense.estimated_cost = Decimal(request.data.get("estimated_cost"))

        if request.data.get('final_cost') and request.data.get('final_cost') != '':
            myexpense.estimated_cost = Decimal(request.data.get("final_cost"))

        if request.data.get('note') and request.data.get('note') != '':
            myexpense.note = request.data.get("note")

        if request.data.get('name') and request.data.get('name') != '':
            myexpense.name = request.data.get("name")

        if request.data.get('category_id') and request.data.get('category_id') != '':
            mycategory = get_budget_category(request.data.get('category_id'))
            if not mycategory:
                return Response(error_response("Invalid Budget Category", '149'), status=HTTP_400_BAD_REQUEST)

            myexpense.category = mycategory

        myexpense.save()

        # update total values of budget category
        update_budget_category(myexpense.category)

        serializer = BudgetExpenseSerializer(myexpense, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_expense_payments')
    def get_expense_payments(self, request, *args, **kwargs):
        """
        Returns expense payments create under a budget expense

        """
        mycategory = self.get_object()
        myqueryset = mycategory.payments.all()
        serializer = ExpensePaymentSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='create_expense_payment')
    def create_expense_payment(self, request, *args, **kwargs):
        """
        creates an expense payment under a budget expense

        """
        payment_date = request.data.get('payment_date', None)
        payment_due = request.data.get('payment_due', None)
        paid_by = request.data.get('paid_by', None)
        is_paid = request.data.get('is_paid', False)
        payment_amount = request.data.get('payment_amount', None)
        payment_method = request.data.get('payment_method', None)
        currency = get_currency(request)

        if not payment_date:
            return Response(error_response("Please provide a payment date", '145'), status=HTTP_400_BAD_REQUEST)

        if payment_due and payment_due != '':
            payment_due = validate_date(payment_due)
            if payment_due is None:
                return Response(error_response("Please provide a valid payment due date", '146'), status=HTTP_400_BAD_REQUEST)

        payment_date = validate_date(payment_date)
        if payment_date is None:
            return Response(error_response("Please provide a valid payment date", '147'), status=HTTP_400_BAD_REQUEST)

        payment_amount = validate_decimal(payment_amount)
        if not payment_amount:
            return Response(error_response("Invalid Payment Amount", '148'), status=HTTP_400_BAD_REQUEST)

        myexpense = self.get_object()

        mypayment = create_expense_payment(payment_date, payment_due, paid_by, myexpense, currency, is_paid, payment_amount, payment_method, request.user)

        # update total values of expense
        update_expense(myexpense)

        # update total values of budget category
        update_budget_category(myexpense.category)

        serializer = ExpensePaymentSerializer(mypayment, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='delete_expense_payments')
    def delete_expense_payment(self, request, *args, **kwargs):
        """
        Deletes an expense payment

        """
        payment_id = request.data.get('payment_id')
        mypayment = get_expense_payment(payment_id)

        myexpense = mypayment.expense

        if mypayment.created_by == request.user:
            mypayment.delete()

        # update total values of expense
        update_expense(myexpense)

        # update total values of budget category
        update_budget_category(myexpense.category)

        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a budget expense

        """
        myexpense = self.get_object()
        budget_category = myexpense.category
        if myexpense.created_by == request.user:
            myexpense.delete()
        # update total values of budget category
        update_budget_category(budget_category)
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class ExpensePayments(APIView):

    def get(self, request, *args, **kwargs):
        myqueryset = ExpensePayment.objects.select_related('expense').filter(expense__category__wedding__id=request.user.wedding_id).order_by('-created_at')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = ExtendedExpensePaymentSerializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

