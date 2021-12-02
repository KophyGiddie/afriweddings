from django.db import models
from apps.weddings.models import Wedding
from django.conf import settings
import uuid


class GuestEvent(models.Model):
    """
    Model for Guest events

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guest_events',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    invited_guests = models.IntegerField(default=0)
    confirmed_guests = models.IntegerField(default=0)
    pending_guests = models.IntegerField(default=0)
    guests_cancelled = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='guest_event',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Guest Events'
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.name)


class GuestGroup(models.Model):
    """
    Model for guest groups

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guest_groups',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_wedding_author = models.BooleanField(default=False)
    wedding_creator_name = models.CharField(max_length=2000, blank=True, null=True)
    wedding_partner_name = models.CharField(max_length=2000, blank=True, null=True)
    is_wedding_partner = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    full_group_name = models.CharField(max_length=2000, blank=True, null=True)
    name = models.CharField(max_length=2000, blank=True, null=True)
    num_of_guests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='guest_group',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Guest Groups'
        ordering = ('-created_at',)

    def get_name(self):
        myname = self.name

        if self.is_wedding_partner:
            myname = "%s's %s" % (self.wedding_partner_name, self.name)

        if self.is_wedding_author:
            myname = "%s's %s" % (self.wedding_creator_name, self.name)

        return myname

    def __str__(self):
        return '%s' % (self.name)


class Guest(models.Model):
    """
    Model for Guests

    # These are guests who will attend the wedding which is different from GUEST as a user type
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guests',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        GuestGroup,
        related_name='guests',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='guests',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=2000, blank=True, null=True)
    last_name = models.CharField(max_length=2000, blank=True, null=True)
    age = models.CharField(max_length=2000, blank=True, null=True)
    address = models.CharField(max_length=2000, blank=True, null=True)
    email = models.CharField(max_length=2000, blank=True, null=True)
    phone = models.CharField(max_length=2000, blank=True, null=True)
    companion = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Guests'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.first_name)


class GuestInvitation(models.Model):
    """
    Model for Guests

    # These are guests who will attend the wedding which is different from GUEST as a user type
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guests_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    event = models.ForeignKey(
        GuestEvent,
        related_name='guests_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    guest = models.ForeignKey(
        Guest,
        related_name='guests_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        GuestGroup,
        related_name='guests_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='guests_invitations',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    invite_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Guests Invitations'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.status)
