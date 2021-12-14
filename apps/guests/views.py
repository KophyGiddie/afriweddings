from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.guests.serializer import (
    GuestGroupSerializer, GuestEventSerializer,
    GuestSerializer, ExtendedGuestGroupSerializer,
    GuestInvitationSerializer, PublicGuestInvitationSerializer
)
from apps.rsvp.serializer import RSVPSerializer
from utils.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from utils.utilities import get_wedding, send_online_invitation_email
from apps.guests.models import GuestGroup, GuestEvent, Guest, GuestInvitation
from apps.guests.helpers import (
    create_guest_event, get_guest_event_by_name,
    create_guest_group, get_guest_group_by_name,
    create_guest, get_guest_group_by_id,
    update_event_guests, get_guest_invitation_by_id,
    get_guest_public_invitation_by_id, get_guest_by_id,
    get_guest_invitations_by_guest_id, bulk_populate_guest_list,
    bulk_assign_guests, get_public_guest_by_id
)
from apps.celerytasks.tasks import send_group_invitation_task


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

    @action(methods=['get'], detail=True, url_path='get_guest_invitations')
    def get_guest_invitations(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        myevent = self.get_object()
        myqueryset = GuestInvitation.objects.select_related('event', 'guest').filter(wedding__id=request.user.wedding_id, event=myevent)
        serializer = GuestInvitationSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


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

    @action(methods=['get'], detail=True, url_path='get_guests')
    def get_guests(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        mygroup = self.get_object()
        myqueryset = Guest.objects.filter(wedding__id=request.user.wedding_id, group=mygroup)
        serializer = GuestSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='send_group_invitation')
    def send_group_invitation(self, request, *args, **kwargs):
        """
        Send Online Invitation to all members in the group

        """
        mygroup = self.get_object()
        mywedding = get_wedding(request)

        send_group_invitation_task.delay(mygroup.id, mywedding.id, request.user.first_name, mywedding.wedding_date)

        serializer = GuestGroupSerializer(mygroup, context={'request': request}, many=False)
        return Response(success_response('Invitation has been sent', serializer.data), status=HTTP_200_OK)

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


class GuestViewSet(viewsets.ModelViewSet):
    model = Guest
    serializer_class = GuestSerializer
    queryset = Guest.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created guest

        """
        myqueryset = Guest.objects.filter(wedding__id=request.user.wedding_id)
        serializer = GuestSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a guest

        """
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        event_ids = request.data.get('event_ids', None)
        group_id = request.data.get('group_id', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)

        if not first_name:
            return Response(error_response("Please provide the first name value", '140'), status=HTTP_400_BAD_REQUEST)

        if not group_id:
            return Response(error_response("Please provide a group", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)

        myguest = create_guest(mywedding, request.user, first_name, last_name, event_ids, group_id, email, phone)

        serializer = GuestSerializer(myguest, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        edits a guest

        """
        myobject = self.get_object()

        if request.data.get('first_name') and request.data.get('first_name') != '':
            myobject.first_name = request.data.get('first_name')

        if request.data.get('last_name') and request.data.get('last_name') != '':
            myobject.last_name = request.data.get('last_name')

        if request.data.get('group_id') and request.data.get('group_id') != '':
            mywedding = get_wedding(request)
            group = get_guest_group_by_id(request.data.get('group_id'), mywedding)
            if group:
                myobject.group = group

        if request.data.get('email') and request.data.get('email') != '':
            myobject.email = request.data.get('email')

        if request.data.get('phone') and request.data.get('phone') != '':
            myobject.phone = request.data.get('phone')

        myobject.save()

        serializer = GuestSerializer(myobject, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='filter_guests_invitations')
    def filter_guests_invitations(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        group_id = request.data.get('group_id')
        myqueryset = GuestGroup.objects.prefetch_related('guests_invitations', 'guests_invitations__event', 'guests_invitations__guest').filter(wedding__id=request.user.wedding_id)
        if group_id and group_id != '':
            myqueryset = myqueryset.filter(id=group_id)
        serializer = ExtendedGuestGroupSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='bulk_assign_event')
    def bulk_assign_event(self, request, *args, **kwargs):
        """
        Update guest invitation by changing its status to confirmed or declined or pending

        """
        guest_ids = request.data.get('guest_ids', None)
        event_ids = request.data.get('event_ids', None)

        mywedding = get_wedding(request)

        bulk_assign_guests(guest_ids, event_ids, mywedding, request.user)

        return Response(success_response('Event Assigned Successfully'), status=HTTP_200_OK)


    @action(methods=['post'], detail=False, url_path='update_guests_invitation')
    def update_guests_invitation(self, request, *args, **kwargs):
        """
        Update guest invitation by changing its status to confirmed or declined or pending

        """
        guest_invitation_id = request.data.get('guest_invitation_id', None)
        status = request.data.get('status', None)

        mywedding = get_wedding(request)

        myobject = get_guest_invitation_by_id(guest_invitation_id, mywedding)
        myobject.status = status
        myobject.save()

        update_event_guests(myobject.event)

        serializer = GuestInvitationSerializer(myobject, context={'request': request}, many=False)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='get_rsvps')
    def get_rsvps(self, request, *args, **kwargs):
        guest_invitation_id = request.data.get('guest_invitation_id', None)
        mywedding = get_wedding(request)
        myobject = get_guest_invitation_by_id(guest_invitation_id, mywedding)
        myqueryset = myobject.rsvp.select_related('rsvp_question').all()
        serializer = RSVPSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='send_online_invitation')
    def send_online_invitation(self, request, *args, **kwargs):
        """
        Update guest invitation by changing its status to confirmed or declined or pending

        """
        guest_id = request.data.get('guest_id', None)
        mywedding = get_wedding(request)

        myobject = get_guest_by_id(guest_id, mywedding)

        if not myobject.email:
            return Response(error_response("This guest does not have an email address", '140'), status=HTTP_400_BAD_REQUEST)

        send_online_invitation_email(guest_id, myobject.first_name, mywedding.author.first_name, mywedding.wedding_date, mywedding.partner_first_name, myobject.email)

        serializer = GuestSerializer(myobject, context={'request': request}, many=False)
        return Response(success_response('Invitation has been sent', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a guest, it also deletes the guest invitation

        """
        myobject = self.get_object()
        if myobject.created_by == request.user:
            myobject.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class VerifyGuestToken(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        guest_id = request.data.get('token', None)
        myobject = get_public_guest_by_id(guest_id)
        serializer = GuestSerializer(myobject, context={'request': request}, many=False)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class UpdateOnlineGuestInvitation(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        guest_invitation_id = request.data.get('token', None)
        status = request.data.get('status', None)

        myobject = get_guest_public_invitation_by_id(guest_invitation_id)
        myobject.status = status
        myobject.save()

        update_event_guests(myobject.event)

        serializer = GuestInvitationSerializer(myobject, context={'request': request}, many=False)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class GetGuestEventInvitations(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        guest_id = request.data.get('token', None)
        myobject = get_guest_invitations_by_guest_id(guest_id)
        serializer = GuestInvitationSerializer(myobject, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class SearchPublicGuest(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        public_url = request.data.get('public_url')

        myqueryset = GuestInvitation.objects.select_related('wedding', 'event', 'guest').filter(wedding__public_url=public_url).order_by('-id')

        if first_name:
            myqueryset = myqueryset.filter(guest__first_name__icontains=first_name)

        if last_name:
            myqueryset = myqueryset.filter(guest__last_name__icontains=last_name)

        if email:
            myqueryset = myqueryset.filter(guest__email__icontains=email)

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = PublicGuestInvitationSerializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)


class BulkUploadGuestList(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        mywedding = get_wedding(request)

        bulk_populate_guest_list(data, mywedding, request.user)

        myqueryset = Guest.objects.filter(wedding__id=request.user.wedding_id)
        serializer = GuestSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
