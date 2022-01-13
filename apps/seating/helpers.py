from apps.seating.models import SeatingTable, SeatingChart
from django.core.exceptions import ValidationError


def create_seating_table(name, mywedding, table_capacity, myuser):
    """
    Creates a seating table

    """
    mytable = SeatingTable.objects.create(
        name=name,
        wedding=mywedding,
        table_capacity=table_capacity,
        created_by=myuser
    )
    return mytable


def create_seating_chart(seat_number, mywedding, myguest, myevent, mytable, myuser):
    """
    Creates a seating table

    """
    mychart = SeatingChart.objects.create(
        seat_number=seat_number,
        wedding=mywedding,
        guest=myguest,
        guest_event=myevent,
        table=mytable,
        created_by=myuser
    )
    return mychart


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
