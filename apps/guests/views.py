from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.guests.serializer import GuestGroupSerializer, GuestEventSerializer
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding, validate_date
from apps.guests.models import GuestGroup, GuestEvent, Guest
from apps.guests.helpers import (
    create_guest_event, get_guest_event_by_name,
    create_guest_group, get_guest_group_by_name
)


class GuestEventViewSet(viewsets.ModelViewSet):
    model = GuestEvent
    serializer_class = GuestEventSerializer
    queryset = GuestEvent.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created guest events

        """
        myqueryset = GuestEvent.objects.filter(wedding__id=request.user.wedding_id)
        serializer = GuestEventSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a guest event

        """
        name = request.data.get('name', None)

        if not name:
            return Response(error_response("Please provide the name value", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)
        existing_event = get_guest_event_by_name(name, mywedding)

        if existing_event:
            return Response(error_response("An event with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        myevent = create_guest_event(name, mywedding, request.user)

        serializer = GuestEventSerializer(myevent, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        edits a guest event

        """
        myevent = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            myevent.name = request.data.get('name')

        myevent.save()

        serializer = GuestEventSerializer(myevent, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a guest event

        """
        myobject = self.get_object()
        if myobject.created_by == request.user:
            myobject.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class GuestGroupViewSet(viewsets.ModelViewSet):
    model = GuestGroup
    serializer_class = GuestGroupSerializer
    queryset = GuestGroup.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created guest groups

        """
        myqueryset = GuestGroup.objects.filter(wedding__id=request.user.wedding_id)
        serializer = GuestGroupSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a guest group

        """
        name = request.data.get('name', None)

        if not name:
            return Response(error_response("Please provide the name value", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)
        existing_category = get_guest_group_by_name(name, mywedding)

        if existing_category:
            return Response(error_response("A group with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        mycategory = create_guest_group(name, mywedding, request.user)

        serializer = GuestGroupSerializer(mycategory, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        edits a guest group

        """
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        mycategory.save()

        serializer = GuestGroupSerializer(mycategory, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a guest group

        """
        myobject = self.get_object()
        if myobject.created_by == request.user:
            myobject.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)
