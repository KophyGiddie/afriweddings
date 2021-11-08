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
from apps.seating.serializer import SeatingTableSerializer
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding
from dateutil.parser import parse
from decimal import Decimal
from apps.seating.models import SeatingTable, SeatingChart


class SeatingTableViewSet(viewsets.ModelViewSet):
    model = SeatingTable
    serializer_class = SeatingTableSerializer
    queryset = SeatingTable.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = SeatingTable.objects.filter(wedding__id=request.user.wedding_id)
        serializer = SeatingTableSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        table_capacity = request.data.get('table_capacity', None)

        mywedding = get_wedding(request)

        mytable = SeatingTable.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  table_capacity=table_capacity,
                                  created_by=request.user
                                )

        serializer = SeatingTableSerializer(mytable, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mytable = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mytable.name = request.data.get('name')

        if request.data.get('table_capacity') and request.data.get('table_capacity') != '':
            mytable.table_capacity = request.data.get('table_capacity')

        mytable.save()

        serializer = SeatingTableSerializer(mytable, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mytable = self.get_object()
        if mytable.created_by == request.user:
            mytable.delete()
        return Response(success_response('Image Deleted Successfully'), status=HTTP_200_OK)
