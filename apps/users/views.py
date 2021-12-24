from utils.responses import error_response, success_response
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.invitations.serializer import InvitationSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.users.serializer import UserSerializer, UserAuthSerializer, UserNotificationSerializer
from apps.users.models import AFUser, FailedLogin, StoredPass, UserNotification
from apps.users.helpers import update_wedding_team_image
from utils.pagination import PageNumberPagination
from rest_framework import viewsets
from apps.invitations.models import Invitation
from utils.utilities import hash_string, send_activation_email, get_client_ip, send_forgot_password_email
from utils.token import account_activation_token
from django.utils import timezone
from apps.weddings.models import WeddingTeam
from dateutil.relativedelta import relativedelta
from apps.celerytasks.tasks import populate_wedding_checklist, compress_image
from apps.prerequisites.models import DefaultChecklistCategory, DefaultChecklistSchedule
from apps.checklists.models import ChecklistCategory, ChecklistSchedule
from rest_framework.decorators import action
from utils.utilities import get_wedding


class SignupUser(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        user_role = request.data.get('user_role')
        user_type = request.data.get('user_type')
        password = request.data.get('password', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        email = request.data.get('email', None)
        invitation_code = request.data.get('invitation_code', None)

        try:
            if password is not None\
                and first_name is not None\
                and last_name is not None\
                and email is not None\
                and user_role is not None:

                user = AFUser.objects.get(email=email)
                return Response(error_response("Email already exist", '101'), status=HTTP_400_BAD_REQUEST)
            else:
                return Response(error_response("Please all supply required parameters", '103'), status=HTTP_400_BAD_REQUEST)

        except AFUser.DoesNotExist:
            user = AFUser(
                        email=email,
                        invitation_code=invitation_code,
                        first_name=first_name,
                        user_type=user_type,
                        user_role=user_role,
                        last_name=last_name,
                        username=email,
                        is_active=False,
                    )
            user.set_password(password)
            user.save()

            if invitation_code and invitation_code is not None and invitation_code != '':
                try:
                    myinvitation = Invitation.objects.get(invitation_code=invitation_code)
                    mywedding = myinvitation.wedding
                    if myinvitation.invitation_type == 'Partner':
                        mywedding.partner = user
                        mywedding.admins.add(user)
                        mywedding.save()

                    elif myinvitation.invitation_type == 'Wedding Team':
                        myteam = WeddingTeam.objects.get(wedding=mywedding, email=email)
                        myteam.member = user
                        myteam.save()

                        user.is_wedding_admin = False
                        user.save()

                        mywedding.wedding_team.add(user)
                        mywedding.save()

                    if user_role == 'Wedding Planner':
                        mywedding.admins.add(user)
                        mywedding.save()

                    user.wedding_id = mywedding.id
                    user.is_active = True
                    user.save()

                    # do has multiple weddings check here
                except Invitation.DoesNotExist:
                    return Response(error_response("Invalid Invitation Code", '102'), status=HTTP_400_BAD_REQUEST)

            else:
                mytoken = account_activation_token.make_token(user)
                user.activation_token = mytoken
                user.save()

                send_activation_email(user, mytoken, "Kindly Activate Your Account")

            hashed = hash_string(password)
            StoredPass.objects.create(hashed=hashed, author=user)

            return Response(success_response('Kindly validate your email'), status=HTTP_200_OK)


class ValidateEmail(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        print (request.data)
        token = request.data.get('token', None)

        try:
            theuser = AFUser.objects.get(activation_token=token)
            theuser.activation_token = ''
            theuser.is_active = True
            theuser.save()

            #Start doing backjobs here
            checklist_categories = DefaultChecklistCategory.objects.all()
            checklist_schedules = DefaultChecklistSchedule.objects.all()

            for item in checklist_categories:
                try:
                    ChecklistCategory.objects.get(created_by=theuser, name=item.name, identifier=item.identifier)
                except ChecklistCategory.DoesNotExist:
                    ChecklistCategory.objects.create(created_by=theuser, name=item.name, identifier=item.identifier)

            for item in checklist_schedules:
                try:
                    ChecklistSchedule.objects.get(created_by=theuser, name=item.name, identifier=item.identifier, priority=item.priority)
                except ChecklistSchedule.DoesNotExist:
                    ChecklistSchedule.objects.create(created_by=theuser, name=item.name, identifier=item.identifier, priority=item.priority)

            myschedules = ChecklistSchedule.objects.filter(created_by=theuser)
            for item in myschedules:
                populate_wedding_checklist.delay(item.identifier, theuser.id)

            return Response(success_response('Your email has been verified successfully kindly login'), status=HTTP_200_OK)
        except AFUser.DoesNotExist:
            return Response(error_response("Invalid Token", '102'), status=HTTP_400_BAD_REQUEST)


class CurrentUserProfile(APIView):

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        profile = request.data
        try:
            serializer = UserSerializer(user, context={'request': request}, data=profile, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
            return Response(error_response("Please all supply required parameters", '103'), status=HTTP_400_BAD_REQUEST)
        except AssertionError:
            print (serializer.errors)
            serializer = UserSerializer(profile, context={'request': request})
            return Response(error_response("An unexpected error happened. Our engineers have been notified and will fix it", '103'), status=HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    def post(self, request, *args, **kwargs):
        password = request.data.get('new_password', None)
        old_password = request.data.get('old_password', None)

        user = authenticate(email=request.user.email, password=old_password)

        if user is None:
            return Response(error_response('Your old password is wrong', '102'), status=HTTP_400_BAD_REQUEST)

        myuser = request.user
        hashed = hash_string(password)
        mypasses = StoredPass.objects.filter(author=myuser)

        for item in mypasses:
            if item.hashed == hashed:
                return Response(error_response("This password has already been used", '106'), status=HTTP_400_BAD_REQUEST)

        myuser.set_password(request.data.get('new_password'))
        myuser.password_changed = True
        myuser.save()

        serializer = UserSerializer(myuser, context={'request': request})
        return Response(success_response('Password Changed Successfully', serializer.data), status=HTTP_200_OK)


class ResendSignupVerification(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        user = AFUser.objects.get(email=email)

        mytoken = account_activation_token.make_token(user)
        print (mytoken)
        user.activation_token = mytoken
        user.save()

        send_activation_email(user, mytoken, "Kindly Activate Your Account")

        return Response(success_response('Email Sent'), status=HTTP_200_OK)


class ForgotPassword(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            myuser = AFUser.objects.get(email=email)
            mytoken = account_activation_token.make_token(myuser)
            myuser.activation_token = mytoken
            myuser.email_initiation_date = timezone.now()
            myuser.save()

            title = 'Afriweddings Password Reset'

            send_forgot_password_email(myuser, mytoken, title)

            return Response(success_response('Please check your email for the password reset instructions',), status=HTTP_200_OK)

        except AFUser.DoesNotExist:
            return Response(error_response("Email doesn't exist", '110'), status=HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        password = request.data.get('password', None)
        activation_token = request.data.get('token', None)

        try:
            myuser = AFUser.objects.get(activation_token=activation_token)
            new_date = timezone.now() - relativedelta(days=2)

            if myuser.email_initiation_date < new_date:
                return Response(error_response("Your Linked has Expired. Contact Admin", '110'), status=HTTP_400_BAD_REQUEST)

        except AFUser.DoesNotExist:
            return Response(error_response("Invalid Token", '110'), status=HTTP_400_BAD_REQUEST)

        hashed = hash_string(password)
        mypasses = StoredPass.objects.filter(author=myuser)

        for item in mypasses:
            if item.hashed == hashed:
                return Response(error_response("This password has already been used", '110'), status=HTTP_400_BAD_REQUEST)

        myuser.set_password(password)
        myuser.wild_string = ''
        myuser.password_changed = True
        myuser.save()

        return Response(success_response('Password Reset Successfully. Kindly login'), status=HTTP_200_OK)


class LoginUser(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password', None)

        if not email:
            return Response(error_response("Please provide the email value", '112'), status=HTTP_400_BAD_REQUEST)

        if not password:
            return Response(error_response("Please provide the password value", '113'), status=HTTP_400_BAD_REQUEST)

        try:
            myuser = AFUser.objects.get(email=email)

            #checks if the user is blocked and reverts a message or reset the temporal login fails and unblock if time exceeds
            if myuser.is_blocked:
                cooloff = (timezone.now() - myuser.failed_login_attempts.all().latest('id').date_created).seconds
                if cooloff > 300:
                    myuser.is_blocked = False
                    myuser.temporal_login_fails = 0
                    myuser.save()
                else:
                    left = int(300) - int(cooloff)
                    return Response(error_response('You have attempted to login 3 times unsuccessfully. Your account is locked for %s seconds' % left, '114'), status=HTTP_400_BAD_REQUEST)

            user = authenticate(email=email, password=password)

            #if user credentials passes authentication do OAuth login here
            if user is not None:
                if user.is_active:
                    login(request, user)
                    serializer = UserAuthSerializer(user, context={'request': request})
                    return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
                else:
                    if user.is_blocked:
                        return Response(error_response('Your account has been blocked. Please Contact Provident Insurance Support', '114'), status=HTTP_400_BAD_REQUEST)

            # if user credentials fails increase failed login attempts counter
            else:
                FailedLogin.objects.create(author=myuser, ip_address=get_client_ip(request))
                myuser.temporal_login_fails += 1
                myuser.save()

                if int(myuser.temporal_login_fails) == 3:
                    myuser.is_blocked = True
                    myuser.permanent_login_fails += 1
                    myuser.save()

                    if int(myuser.permanent_login_fails) >= 3:
                        myuser.is_active = False
                        myuser.save()

                    return Response(error_response("You have attempted to login 3 times, with no success. Your account has been locked temporarily for 300 seconds", '111'), status=HTTP_400_BAD_REQUEST)
                left = 3 - myuser.temporal_login_fails
                return Response(error_response('Your Password is incorrect. %s tries left' % left, '115'), status=HTTP_400_BAD_REQUEST)

        except AFUser.DoesNotExist:
            return Response(error_response("Email doesn't exist", '110'), status=HTTP_400_BAD_REQUEST)


class UpdateProfilePicture(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            avatar = request.FILES.get('profile_picture', None)
            invitation_id = request.data.get('invitation_id', None)
            if invitation_id:
                wedding_team_image = request.FILES.get('wedding_team_image', None)
                myinvitation = Invitation.objects.get(id=invitation_id)
                myinvitation.profile_picture = wedding_team_image
                myinvitation.save()

                serializer = InvitationSerializer(myinvitation, context={'request': request})
                return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
            else:
                user.profile_picture = avatar
                user.save()

                # update image in wedding teams associated
                myinvitations = Invitation.objects.filter(email=request.user.email)
                if myinvitations:
                    for myinvitation in myinvitations:
                        myinvitation.profile_picture = user.profile_picture
                        myinvitation.save()

                serializer = UserSerializer(user, context={'request': request})
                # compress_image_choice(user.avatar)
                compress_image.delay(str(user.profile_picture))
                return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
        except ValueError:
            return Response(error_response("Unable to Save Image", '120'), status=HTTP_400_BAD_REQUEST)


class UserNotificationsViewSet(viewsets.ModelViewSet):

    model = UserNotification
    serializer_class = UserNotificationSerializer
    queryset = UserNotification.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = UserNotification.objects.filter(user_in_question=request.user)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = UserNotificationSerializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=True, url_path='mark_as_read')
    def mark_as_read(self, request, *args, **kwargs):
        mynotification = self.get_object()
        mynotification.read = True
        mynotification.save()
        post = UserNotificationSerializer(mynotification, context={'request': request}, many=False)
        return Response(success_response(message="Password Reset Successful", data=post.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='num_of_unread')
    def num_of_unread(self, request, *args, **kwargs):
        mynumber = UserNotification.objects.filter(read=False, user_in_question=request.user).count()
        return Response({'num_of_unread': mynumber,
                         'response_code': '100',
                         'message': 'Data Returned Successfully'}, status=HTTP_200_OK)
