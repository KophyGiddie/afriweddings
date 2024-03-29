from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.users.helpers import create_notification
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.invitations.serializer import InvitationSerializer
from apps.celerytasks.tasks import send_beta_email_task
from apps.weddings.serializer import PublicWeddingSerializer
from utils.pagination import PageNumberPagination
from apps.invitations.models import Invitation, BetaInvitation
from utils.utilities import get_wedding, send_invitation_email, generate_invitation_code
from apps.users.helpers import get_user_by_email
from apps.weddings.models import WeddingRole, Wedding, WeddingTeam, WeddingUserRole
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
        mypicture = request.FILES.get('profile_picture', None)

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
                profile_picture=mypicture
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
                        profile_picture=mypicture,
                        role=myrole
                    )

        send_invitation_email(myinvitation, first_name)
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='delete_wedding_team_member')
    def delete_wedding_team_member(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        invitation_id = request.data.get('wedding_team_id')
        myinvitation = Invitation.objects.get(id=invitation_id)
        mywedding = get_wedding(request)
        try:
            myteam = WeddingTeam.objects.get(email=myinvitation.email, wedding=mywedding)

            if myteam.member:
                myuser = myteam.member
                myuser.wedding_id = ''
                myuser.save()

                try:
                    WeddingUserRole.objects.get(
                        wedding=mywedding,
                        user=myuser
                    ).delete()

                except WeddingUserRole.DoesNotExist:
                    pass

                mywedding.wedding_team.remove(myuser)

            myteam.delete()

        except WeddingTeam.DoesNotExist:
            myteam = None

        myinvitation.delete()

        return Response(success_response('Deleted Successfully', []), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='update_details')
    def update_details(self, request, *args, **kwargs):
        """
        Returns guests invitations

        """
        mypicture = request.FILES.get('profile_picture')
        description = request.data.get('description')
        invitation_id = request.data.get('invitation_id')
        myinvitation = Invitation.objects.get(id=invitation_id)

        try:
            myteam = WeddingTeam.objects.get(email=myinvitation.email, wedding=get_wedding(request))
        except WeddingTeam.DoesNotExist:
            myteam = None

        if mypicture:
            print ('one')
            myinvitation.profile_picture = mypicture
            myinvitation.save()
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


class UpdateWeddingTeamProfilePicture(APIView):
    def post(self, request, *args, **kwargs):
        description = request.data.get('description')
        invitation_id = request.data.get('invitation_id')
        mypicture = request.FILES.get('profile_picture')
        myinvitation = Invitation.objects.get(id=invitation_id)

        try:
            myteam = WeddingTeam.objects.get(email=myinvitation.email, wedding=get_wedding(request))
        except WeddingTeam.DoesNotExist:
            myteam = None

        if mypicture:
            print ('one')
            myinvitation.profile_picture = mypicture
            myinvitation.save()
            if myteam:
                print ('two')
                myteam.profile_picture = mypicture
                myteam.save()

        if description and description != '':
            myinvitation.description = description
            if myteam:
                myteam.description = description
                myteam.save()

        myinvitation.save()

        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class AcceptInvite(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        invitation_code = request.data.get('invitation_code', None)
        user_exists = False
        try:
            myinvitation = Invitation.objects.get(invitation_code=invitation_code)
            myuser = get_user_by_email(myinvitation.email)
            if myuser:
                try:
                    user_exists = True
                    myteam = WeddingTeam.objects.get(wedding=myinvitation.wedding, email=myinvitation.email)
                    myteam.member = myuser
                    myteam.save()
                    mywedding = myinvitation.wedding
                    mywedding.wedding_team.add(myuser)
                    mywedding.save()
                    myuser.has_multiple_weddings = True
                    myuser.save()

                    WeddingUserRole.objects.create(
                        role=myinvitation.invitee_role.role,
                        wedding=myinvitation.wedding,
                        user=myuser
                    )
                except WeddingTeam.DoesNotExist:
                    pass
        except Invitation.DoesNotExist:
            return Response(error_response("Invalid Invitation", '122'), status=HTTP_400_BAD_REQUEST)

        myinvitation.status = 'ACCEPTED'
        myinvitation.save()

        myrole = myinvitation.invitee_role
        if myrole.role == 'Groom' or myrole.role == 'Bride':
            mywedding = myinvitation.wedding
            mywedding.partner_accepted_invite = True
            mywedding.save()

        title = 'Invitation Response'
        body = '%s accepted invitation' % myinvitation.first_name
        create_notification(title, body, None, str(myinvitation.id), myinvitation.wedding.id)
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response({"response_code": "100",
                         "user_exist": user_exists,
                         "message": "Data returned successfully",
                         "results": serializer.data}, status=HTTP_200_OK)


class WeddingsInvitedTo(APIView):

    def get(self, request, *args, **kwargs):
        myids = Invitation.objects.filter(email=request.user.email).values_list('wedding__id', flat=True)
        myqueryset = Wedding.objects.filter(id__in=myids)
        serializer = PublicWeddingSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class SendBetaInvite(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        try:
            BetaInvitation.objects.get(email=email)
            return Response(error_response("User Already Invited", '123'), status=HTTP_400_BAD_REQUEST)

        except BetaInvitation.DoesNotExist:
            BetaInvitation.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            send_beta_email_task.delay(first_name, email)
            return Response(success_response('User Invited Successfully'), status=HTTP_200_OK)


class InviteCouple(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        invitation_type = "COUPLE"
        user_role = request.data.get('role', None)
        if user_role == 'GROOM':
            user_role = 'Groom'
        elif user_role == 'BRIDE':
            user_role = 'Bride'
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        wedding_id = request.data.get('wedding_id', None)


        myids = Wedding.objects.filter(Q(admins=request.user) | Q(planner=request.user)| Q(author=request.user)|Q(wedding_team=request.user)).distinct('id').values_list('id', flat=True)
        
        if wedding_id not in myids:
            return Response(error_response("You dont have access to this wedding", '123'), status=HTTP_400_BAD_REQUEST)
        
        mywedding = get_wedding_by_id(wedding_id)

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
                wedding=mywedding,
                status='PENDING',
                invited_by=request.user,
            )

        send_invitation_email(myinvitation, first_name)
        serializer = InvitationSerializer(myinvitation, context={'request': request})
        return Response(success_response('Invited Successfully', serializer.data), status=HTTP_200_OK)

