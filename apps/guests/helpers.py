from apps.guests.models import GuestGroup, GuestEvent, Guest, GuestInvitation
from django.core.exceptions import ValidationError


def create_guest_invitation(mywedding, myevent, myguest, myuser):
    GuestInvitation.objects.create(
        wedding=mywedding,
        event=myevent,
        guest=myguest,
        created_by=myuser,
        status='',
    )


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


def get_guest_invitations_by_guest_id(myid):
    """
    Returns budget expense using the name

    """
    myguestinvites = GuestInvitation.objects.filter(guest__id=myid)
    return myguestinvites


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


def get_public_guest_by_id(myid):
    """
    Returns budget category using the name

    """
    try:
        myguest = Guest.objects.get(id=myid)
        return myguest
    except Guest.DoesNotExist:
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


def get_guests_by_group_id(group_id, wedding_id):
    """
    Returns budget category using the name

    """
    try:
        myguests = Guest.objects.filter(group__id=group_id, wedding__id=wedding_id)
        return myguests
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


def update_group_guests_count(mygroup_id, mywedding):
    """
    Update expenses total_paid when a payment is made

    """
    mygroup = get_guest_group_by_id(mygroup_id, mywedding)
    total_guests = mywedding.guests.filter(group=mygroup).count()
    mygroup.num_of_guests = total_guests
    mygroup.save()


def update_group_guests(mygroup):
    """
    Update expenses total_paid when a payment is made

    """
    mywedding = mygroup.wedding
    total_guests = mywedding.guests.filter(group=mygroup).count()
    mygroup.num_of_guests = total_guests
    mygroup.save()


def update_event_guests(myevent):
    """
    Update expenses total_paid when a payment is made

    """
    mywedding = myevent.wedding

    total_guests_invited = mywedding.guests.all().count()
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


def update_guest_groups_and_events(mywedding):

    mygroups = mywedding.guest_groups.all()
    for mygroup in mygroups:
        total_guests = mywedding.guests.filter(group=mygroup).count()
        mygroup.num_of_guests = total_guests
        mygroup.save()

    total_guests_invited = mywedding.guests.all().count()
    mywedding.invited_guests = total_guests_invited
    mywedding.save()

    myevents = mywedding.guest_events.all()

    for myevent in myevents:
        myevent.invited_guests = mywedding.guests_invitations.filter(event=myevent).count()
        myevent.save()


def create_guest_custom(mywedding, myuser, first_name, last_name, event_ids, group_id, email, phone, country_code):
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
        country_code=country_code,
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
                                           status='',
                                           group=mygroup)

            if myevent:
                update_event_guests(myevent)

    if group_id and group_id != '':
        update_group_guests(mygroup)

    return myguest


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
                                           status='',
                                           group=mygroup)

            if myevent:
                update_event_guests(myevent)

    if group_id and group_id != '':
        update_group_guests(mygroup)

    return myguest


def bulk_assign_guests(guest_ids, event_ids, mywedding, myuser):
    for item in event_ids:
        myevent = get_guest_event_by_id(item, mywedding)
        print (myevent)
        for element in guest_ids:
            myguest = get_guest_by_id(element, mywedding)
            create_guest_invitation(mywedding, myevent, myguest, myuser)
        update_event_guests(myevent)


def bulk_populate_guest_list(data, mywedding, myuser):
    for item in data:
        create_guest(mywedding, myuser, item.get('first_name'), item.get('last_name'), [], None, item.get('email'), item.get('phone_number'))


def update_guests_invitations(event_ids, myobject, mywedding, myuser):
    guests_invitations = myobject.guests_invitations.all()

    if guests_invitations:

        # DELETE EXISTING INVITATIONS THAT ARE NOT PART OF CURRENT LIST NOW
        guests_invitations.exclude(id__in=event_ids).delete()

        for item in event_ids:
            try:
                GuestInvitation.objects.get(id=item)
            except (GuestInvitation.DoesNotExist, ValidationError):
                myevent = get_guest_event_by_id(item, mywedding)
                myguest = myobject
                create_guest_invitation(mywedding, myevent, myguest, myuser)

            update_event_guests(myevent)
    else:
        for item in event_ids:
            myevent = get_guest_event_by_id(item, mywedding)
            myguest = myobject
            create_guest_invitation(mywedding, myevent, myguest, myuser)
            update_event_guests(myevent)

