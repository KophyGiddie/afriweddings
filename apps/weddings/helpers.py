from apps.weddings.models import WeddingRole


def get_role_by_name(role, wedding):
    try:
        WeddingRole.objects.get(role=role, wedding=wedding)
        return True
    except WeddingRole.DoesNotExist:
        return None
