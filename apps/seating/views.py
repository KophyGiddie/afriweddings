from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.seating.serializer import SeatingTableSerializer, SeatingChartSerializer
from utils.utilities import get_wedding
from apps.seating.models import SeatingTable, SeatingChart
from apps.guests.helpers import get_guest_by_id, get_guest_event_by_id
from apps.seating.helpers import (
    get_seating_table_by_name, get_seating_table_by_id, get_existing_seating_chart,
    create_seating_table, create_seating_chart
)


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

        existing_table = get_seating_table_by_name(name, mywedding)

        if existing_table:
            return Response(error_response("A table with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        mytable = create_seating_table(name, mywedding, table_capacity, request.user)

        serializer = SeatingTableSerializer(mytable, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mytable = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mytable.name = request.data.get('name')

        if request.data.get('table_capacity') and request.data.get('table_capacity') != '':
            mytable.table_capacity = request.data.get('table_capacity')

        mytable.save()

        serializer = SeatingTableSerializer(mytable, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mytable = self.get_object()
        if mytable.created_by == request.user:
            mytable.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class SeatingChartViewSet(viewsets.ModelViewSet):
    model = SeatingChart
    serializer_class = SeatingChartSerializer
    queryset = SeatingChart.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = SeatingChart.objects.select_related('guest', 'table').filter(table__wedding__id=request.user.wedding_id)
        serializer = SeatingChartSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        seat_number = request.data.get('seat_number', None)
        guest_id = request.data.get('guest_id', None)
        event_id = request.data.get('event_id', None)
        table_id = request.data.get('table_id', None)

        mywedding = get_wedding(request)

        myguest = get_guest_by_id(guest_id, mywedding)
        myevent = get_guest_event_by_id(event_id, mywedding)
        mytable = get_seating_table_by_id(table_id, mywedding)

        existing_table = get_existing_seating_chart(myguest, mytable, myevent)

        if existing_table:
            return Response(error_response("This guest is already on this table for this event", '139'), status=HTTP_400_BAD_REQUEST)

        mychart = create_seating_chart(seat_number, mywedding, myguest, myevent, mytable, request.user)

        serializer = SeatingChartSerializer(mychart, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mytable = self.get_object()

        if request.data.get('seat_number') and request.data.get('seat_number') != '':
            mytable.seat_number = request.data.get('seat_number')

        mytable.save()

        serializer = SeatingChartSerializer(mytable, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mytable = self.get_object()
        if mytable.created_by == request.user:
            mytable.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)