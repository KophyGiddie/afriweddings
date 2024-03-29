from apps.users.models import AFUser, UserNotification
from apps.invitations.models import Invitation
from django.core.exceptions import ValidationError


def get_user_by_email(email):
    try:
        return AFUser.objects.get(email=email)
    except (AFUser.DoesNotExist, ValidationError):
        return None


def update_wedding_team_image(avatar, request, wedding):
    try:
        myinvitation = Invitation.objects.get(wedding=wedding, email=request.user.email)
        myinvitation.profile_picture = avatar
        myinvitation.save()
    except Invitation.DoesNotExist:
        print ("pass")
        pass


def create_notification(title, body, myuser, object_id, wedding_id):
    UserNotification.objects.create(user_in_question=myuser,
                                    title=title,
                                    wedding_id=wedding_id,
                                    object_id=object_id,
                                    message=body,
                                    notification_type='GENERAL')
    return True
