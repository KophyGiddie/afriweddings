from apps.users.models import AFUser
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
