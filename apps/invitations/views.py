from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.invitations.serializer import InvitationSerializer
from utils.pagination import PageNumberPagination
from apps.invitations.models import Invitation
from utils.utilities import get_wedding, send_invitation_email, generate_invitation_code
from apps.weddings.models import WeddingRole, Wedding, WeddingTeam
from rest_framework.decorators import action


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
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        mywedding = get_wedding(request)

        try:
            myrole = WeddingRole.objects.get(role=user_role, wedding=mywedding)
        except WeddingRole.DoesNotExist:
            return Response(error_response("Invalid Wedding Role", '123'), status=HTTP_400_BAD_REQUEST)

        try:
            Invitation.objects.get(email=email, wedding=Wedding.objects.get(id=request.user.wedding_id))
            return Response(error_response("This user has already been invited", '121'), status=HTTP_400_BAD_REQUEST)
        except Invitation.DoesNotExist:
            myinvitation = Invitation.objects.create(
                                      invitation_type=invitation_type,
                                      user_type=invitation_type,
                                      invitation_code=generate_invitation_code(),
                                      first_name=first_name,
                                      last_name=last_name,
                                      invitee_role=myrole,
                                      user_role=myrole.role,
                                      email=email,
                                      wedding=get_wedding(request),
                                      status='PENDING',
                                      invited_by=request.user,
                                    )
            if invitation_type == 'Wedding Team':
                try:
                    WeddingTeam.objects.get(email=email, wedding=mywedding)
                except WeddingTeam.DoesNotExist:
                    WeddingTeam.objects.create(
                        wedding=get_wedding(request),
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        role=myrole
                    )
        send_invitation_email(myinvitation, first_name)
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='edit_details')
    def edit_details(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        mypicture = request.FILES.get('picture')
        description = request.data.get('description')
        invitation_id = request.data.get('invitation_id')
        myinvitation = Invitation.objects.get(id=invitation_id)

        try:
            myteam = WeddingTeam.objects.get(email=myinvitation.email, wedding=get_wedding(request))
        except WeddingTeam.DoesNotExist:
            myteam = None

        if mypicture:
            print ('one')
            myinvitation.picture = mypicture
            if myteam:
                print ('two')
                myteam.picture = mypicture
                myteam.save()

        if description and description != '':
            myinvitation.description = description
            if myteam:
                myteam.description = description
                myteam.save()

        myinvitation.save()

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
        myrole = myinvitation.invitee_role
        if myrole.role == 'Groom' or myrole.role == 'Bride':
            mywedding = myinvitation.wedding
            mywedding.partner_accepted_invite = True
            mywedding.save()
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
