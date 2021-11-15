from apps.seating.models import SeatingTable
from django.core.exceptions import ValidationError


def get_seating_table_by_name(name, wedding):
    try:
        SeatingTable.objects.get(name=name, wedding=wedding)
        return True
    except (SeatingTable.DoesNotExist, ValidationError):
        return None
