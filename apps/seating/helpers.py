from apps.seating.models import SeatingTable, SeatingChart
from django.core.exceptions import ValidationError


def get_seating_table_by_name(name, wedding):
    try:
        mytable = SeatingTable.objects.get(name=name, wedding=wedding)
        return mytable
    except (SeatingTable.DoesNotExist, ValidationError):
        return None


def get_seating_table_by_id(myid, wedding):
    try:
        mytable = SeatingTable.objects.get(id=myid, wedding=wedding)
        return mytable
    except (SeatingTable.DoesNotExist, ValidationError):
        return None


def get_existing_seating_chart(myguest, mytable, myevent):
    try:
        mychart = SeatingChart.objects.get(guest=myguest, guest_event=myevent, table=mytable)
        return mychart
    except (SeatingTable.DoesNotExist, ValidationError):
        return None
