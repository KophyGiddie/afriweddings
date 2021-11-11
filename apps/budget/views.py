from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_200_OK,
                                   HTTP_304_NOT_MODIFIED,
                                   HTTP_400_BAD_REQUEST, HTTP_400_BAD_REQUEST)
from apps.budget.serializer import BudgetCategorySerializer, BudgetExpenseSerializer, ExpensePaymentSerializer
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding, validate_date
from apps.budget.helpers import update_expense, update_budget_category, get_currency, validate_decimal
from dateutil.parser import parse
from decimal import Decimal
from apps.budget.models import ExpensePayment, BudgetCategory, BudgetExpense


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    model = BudgetCategory
    serializer_class = BudgetCategorySerializer
    queryset = BudgetCategory.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = BudgetCategory.objects.filter(wedding__id=request.user.wedding_id)
        serializer = BudgetCategorySerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)

        if not name:
            return Response(error_response("Please provide the name value", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)

        mycategory = BudgetCategory.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  total_estimated_cost=Decimal(0),
                                  total_final_cost=Decimal(0),
                                  total_paid=Decimal(0),
                                  total_pending=Decimal(0),
                                  currency=get_currency(request),
                                  created_by=request.user
                                )

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        mycategory.save()

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_expenses')
    def get_expenses(self, request, *args, **kwargs):
        mycategory = self.get_object()
        myqueryset = mycategory.budget_expense.select_related('category').all()
        serializer = BudgetExpenseSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mycategory = self.get_object()
        if mycategory.created_by == request.user:
            mycategory.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class BudgetExpenseViewSet(viewsets.ModelViewSet):
    model = BudgetExpense
    serializer_class = BudgetExpenseSerializer
    queryset = BudgetExpense.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = BudgetExpense.objects.select_related('category').filter(wedding__id=request.user.wedding_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = self.get_serializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
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

        mycategory = BudgetCategory.objects.get(id=category_id)

        myexpense = BudgetExpense.objects.create(
                                  name=name,
                                  category=mycategory,
                                  currency=currency,
                                  estimated_cost=Decimal(estimated_cost),
                                  final_cost=Decimal(final_cost),
                                  paid=Decimal(0),
                                  pending=Decimal(0),
                                  pending=pending,
                                  created_by=request.user
                                )

        update_budget_category(mycategory)

        serializer = BudgetExpenseSerializer(myexpense, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        myexpense = self.get_object()

        if request.data.get('estimated_cost') and request.data.get('estimated_cost') != '':
            myexpense.estimated_cost = Decimal(request.data.get("estimated_cost"))

        if request.data.get('final_cost') and request.data.get('final_cost') != '':
            myexpense.estimated_cost = Decimal(request.data.get("final_cost"))

        if request.data.get('note') and request.data.get('note') != '':
            myexpense.note = request.data.get("note")

        myexpense.save()

        update_budget_category(myexpense.category)

        serializer = BudgetCategorySerializer(myexpense, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_expense_payments')
    def get_expense_payments(self, request, *args, **kwargs):
        mycategory = self.get_object()
        myqueryset = mycategory.payments.all()
        serializer = ExpensePaymentSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='create_expense_payment')
    def create_expense_payment(self, request, *args, **kwargs):
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

        mypayment = ExpensePayment.objects.create(
                                  payment_date=payment_date,
                                  payment_due=payment_due,
                                  paid_by=paid_by,
                                  expense=myexpense,
                                  currency=currency,
                                  is_paid=is_paid,
                                  payment_amount=Decimal(payment_amount),
                                  payment_method=payment_method,
                                  created_by=request.user
                                  )

        update_expense(myexpense)

        update_budget_category(myexpense.category)

        serializer = ExpensePaymentSerializer(mypayment, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['delete'], detail=True, url_path='get_expense_payments')
    def delete_expense_payment(self, request, *args, **kwargs):
        payment_id = request.data.get('payment_id')
        mypayment = ExpensePayment.objects.get(id=payment_id)
        if mypayment.created_by == request.user:
            mypayment.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        mycategory = self.get_object()
        if mycategory.created_by == request.user:
            mycategory.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)

