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
from apps.budget.serializer import BudgetCategorySerializer, BudgetExpenseSerializer
from utils.pagination import PageNumberPagination
from apps.weddings.models import Wedding
from dateutil.parser import parse
from apps.budget.models import BudgetCategory, BudgetExpense


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    model = BudgetCategory
    serializer_class = BudgetCategorySerializer
    queryset = BudgetCategory.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = BudgetCategory.objects.get(wedding_id=request.user.wedding_id)
        serializer = BudgetCategorySerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        currency = request.data.get('currency', None)

        mywedding = Wedding.objects.get(id=request.user.wedding_id)

        mycategory = BudgetCategory.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  currency=currency,
                                  created_by=request.user
                                )

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        if request.data.get('currency') and request.data.get('currency'):
            mycategory.currency = request.data.get("currency")

        mycategory.save()

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='get_expenses')
    def get_expenses(self, request):
        mycategory = self.get_object()
        myqueryset = mycategory.budget_expense.select_related('category').all()
        serializer = BudgetExpenseSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mycategory = self.get_object()
        if mycategory.author == request.user:
            mycategory.delete()
        return Response(success_response('Image Deleted Successfully'), status=HTTP_200_OK)


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
        currency = request.data.get('currency', None)
        estimated_cost = request.data.get('estimated_cost', None)

        mywedding = Wedding.objects.get(id=request.user.wedding_id)

        mycategory = BudgetExpense.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  category=BudgetCategory.objects.get(id=category_id),
                                  currency=currency,
                                  estimated_cost=estimated_cost,
                                  created_by=request.user
                                )

        serializer = BudgetExpenseSerializer(mycategory, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mycategory = self.get_object()

        if request.data.get('paid') and request.data.get('paid') != '':
            mycategory.paid = request.data.get('paid')

        if request.data.get('estimated_cost') and request.data.get('estimated_cost'):
            mycategory.estimated_cost = request.data.get("estimated_cost")

        mycategory.save()

        serializer = BudgetCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)



    def delete(self, request, *args, **kwargs):
        return Response(error_response("Invalid Operation", '123'), status=HTTP_400_BAD_REQUEST)
