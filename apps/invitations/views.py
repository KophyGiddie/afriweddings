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
from apps.invitations.serializer import InvitationSerializer
from utils.pagination import PageNumberPagination
from apps.invitations.models import Invitation
from utils.utilities import get_wedding, send_invitation_email, generate_invitation_code
from apps.weddings.models import WeddingRole, Wedding


class InvitationViewSet(viewsets.ModelViewSet):
    model = Invitation
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.select_related('invitee_role').all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = Invitation.objects.select_related('invitee_role').filter(wedding__id=request.user.wedding_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = self.get_serializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        invitation_type = request.data.get('invitation_type', None)
        user_role = request.data.get('user_role', None)

        if invitation_type == 'Partner':
            myrole = WeddingRole.objects.get(role=user_role)
        else:
            myrole = WeddingRole.objects.get(id=user_role)

        try:
            Invitation.objects.get(email=email, wedding=Wedding.objects.get(id=request.user.wedding_id))
            return Response(error_response("This user has already been invited", '121'), status=HTTP_400_BAD_REQUEST)
        except Invitation.DoesNotExist:
            myinvitation = Invitation.objects.create(
                                      invitation_type=invitation_type,
                                      invitation_code=generate_invitation_code(),
                                      invitee_role=myrole,
                                      user_role=myrole.role,
                                      email=email,
                                      wedding=get_wedding(request),
                                      status='PENDING_ACCEPTANCE',
                                      invited_by=request.user,
                                    )

        send_invitation_email(myinvitation)
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(error_response("Invalid Operation", '123'), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response(error_response("Invalid Operation", '123'), status=HTTP_400_BAD_REQUEST)


class AcceptInvite(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        invitation_code = request.data.get('invitation_code', None)
        try:
            myinvitation = Invitation.objects.get(invitation_code=invitation_code)
        except Invitation.DoesNotExist:
            return Response(error_response("Invalid Invitation", '122'), status=HTTP_400_BAD_REQUEST)
        myinvitation.status = 'ACCEPTED'
        myinvitation.save()
        return Response(success_response('Invite Accepted Successfully'), status=HTTP_200_OK)
