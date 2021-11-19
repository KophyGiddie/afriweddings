from apps.guests.models import GuestGroup, GuestEvent
from django.core.exceptions import ValidationError


def get_guest_event_by_name(name, wedding):
    """
    Returns budget expense using the name

    """
    try:
        GuestEvent.objects.get(name=name, wedding=wedding)
        return True
    except GuestEvent.DoesNotExist:
        return None


def get_guest_group_by_name(name, wedding):
    """
    Returns budget category using the name

    """
    try:
        GuestGroup.objects.get(name=name, wedding=wedding)
        return True
    except GuestGroup.DoesNotExist:
        return None


def create_guest_event(name, mywedding, myuser):
    """
    Creates a guest event with the parameters supplied

    """
    myevent = GuestEvent.objects.create(
        name=name,
        wedding=mywedding,
        num_of_guests=0,
        created_by=myuser
    )
    return myevent


def create_guest_group(name, mywedding, myuser):
    """
    Creates a guest group with the parameters supplied

    """
    mygroup = GuestGroup.objects.create(
        name=name,
        full_group_name=name,
        wedding=mywedding,
        num_of_guests=0,
        created_by=myuser
    )
    return mygroup

