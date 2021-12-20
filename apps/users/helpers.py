from apps.users.models import AFUser
from django.core.exceptions import ValidationError


def get_user_by_email(email):
    try:
        return AFUser.objects.get(email=email)
    except (AFUser.DoesNotExist, ValidationError):
        return None
