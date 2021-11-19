from apps.guests.models import GuestGroup, GuestEvent
from django.core.exceptions import ValidationError
from django.db.models import Sum


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


def update_group_guests(mygroup):
    """
    Update expenses total_paid when a payment is made

    """
    mywedding = mygroup.wedding

    total_guests = mywedding.guests_invitations.filter(group=mygroup).count()
    mygroup.num_of_guests = total_guests
    mygroup.save()


def update_event_guests(myevent):
    """
    Update expenses total_paid when a payment is made

    """
    mywedding = myevent.wedding

    total_guests_invited = mywedding.guests_invitations.all().count()
    guests_confirmed = mywedding.guests_invitations.filter(status='CONFIRMED').count()
    guests_cancelled = mywedding.guests_invitations.filter(status='CANCELLED').count()
    guests_pending = mywedding.guests_invitations.filter(status='PENDING').count()

    mywedding.invited_guests = total_guests_invited
    mywedding.confirmed_guests = guests_confirmed
    mywedding.pending_guests = guests_pending
    mywedding.guests_cancelled = guests_cancelled

    mywedding.save()

    myevent.invited_guests = mywedding.guests_invitations.filter(event=myevent).count()
    myevent.confirmed_guests = mywedding.guests_invitations.filter(status='CONFIRMED', event=myevent).count()
    myevent.pending_guests = mywedding.guests_invitations.filter(status='CANCELLED', event=myevent).count()
    myevent.guests_cancelled = mywedding.guests_invitations.filter(status='PENDING', event=myevent).count()
    myevent.save()


def create_guest(name, mywedding, myuser):
    """
    Creates a guest event with the parameters supplied

    """
    myguest = GuestEvent.objects.create(
        name=name,
        wedding=mywedding,
        num_of_guests=0,
        created_by=myuser
    )

    update_group_guests(mygroup)

    update_event_guests(myevent)

    return myguest

