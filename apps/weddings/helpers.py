from apps.weddings.models import WeddingRole
from django.core.exceptions import ValidationError


def get_role_by_name(role, wedding):
    try:
        WeddingRole.objects.get(role=role, wedding=wedding)
        return True
    except (WeddingRole.DoesNotExist, ValidationError):
        return None


def generate_slug(mywedding):
    print ('slug')