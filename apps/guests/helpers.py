from apps.guests.models import GuestGroup, GuestEvent, Guest, GuestInvitation
from django.core.exceptions import ValidationError


def get_guest_public_invitation_by_id(myid):
    """
    Returns budget expense using the name

    """
    try:
        myguestinvite = GuestInvitation.objects.get(id=myid)
        return myguestinvite
    except (GuestInvitation.DoesNotExist, ValidationError):
        return None


def get_guest_invitation_by_id(myid, wedding):
    """
    Returns budget expense using the name

    """
    try:
        myguestinvite = GuestInvitation.objects.get(id=myid, wedding=wedding)
        return myguestinvite
    except (GuestInvitation.DoesNotExist, ValidationError):
        return None


def get_guest_event_by_id(myid, wedding):
    """
    Returns budget expense using the name

    """
    try:
        myguestevent = GuestEvent.objects.get(id=myid, wedding=wedding)
        return myguestevent
    except (GuestEvent.DoesNotExist, ValidationError):
        return None


def get_guest_event_by_name(name, wedding):
    """
    Returns budget expense using the name

    """
    try:
        myguestevent = GuestEvent.objects.get(name=name, wedding=wedding)
        return myguestevent
    except GuestEvent.DoesNotExist:
        return None


def get_guest_group_by_id(myid, wedding):
    """
    Returns budget category using the name

    """
    try:
        mygroup = GuestGroup.objects.get(id=myid, wedding=wedding)
        return mygroup
    except (GuestGroup.DoesNotExist, ValidationError):
        return None


def get_guest_group_by_name(name, wedding):
    """
    Returns budget category using the name

    """
    try:
        mygroup = GuestGroup.objects.get(name=name, wedding=wedding)
        return mygroup
    except GuestGroup.DoesNotExist:
        return None


def get_guest_by_id(myid, wedding):
    """
    Returns budget category using the name

    """
    try:
        myguest = Guest.objects.get(id=myid, wedding=wedding)
        return myguest
    except Guest.DoesNotExist:
        return None


def create_guest_event(name, mywedding, myuser):
    """
    Creates a guest event with the parameters supplied

    """
    myevent = GuestEvent.objects.create(
        name=name,
        wedding=mywedding,
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
    myevent.pending_guests = mywedding.guests_invitations.filter(status='PENDING', event=myevent).count()
    myevent.guests_cancelled = mywedding.guests_invitations.filter(status='CANCELLED', event=myevent).count()
    myevent.save()


def create_guest(mywedding, myuser, first_name, last_name, event_ids, group_id, email, phone):
    """
    Creates a guest event with the parameters supplied

    """
    mygroup = None

    if group_id and group_id != '':
        mygroup = get_guest_group_by_id(group_id, mywedding)

    myguest = Guest.objects.create(
        first_name=first_name,
        last_name=last_name,
        wedding=mywedding,
        group=mygroup,
        status='PENDING',
        email=email,
        phone=phone,
        created_by=myuser
    )

    if event_ids:
        for item in event_ids:
            myevent = get_guest_event_by_id(item, mywedding)

            GuestInvitation.objects.create(wedding=mywedding,
                                           event=myevent,
                                           guest=myguest,
                                           created_by=myuser,
                                           status='PENDING',
                                           group=mygroup)

            if myevent:
                update_event_guests(myevent)

    update_group_guests(mygroup)

    return myguest
