from django.db import models
from apps.weddings.models import Wedding
from django.conf import settings
import uuid


class GuestEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guest_events',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Guest Events'
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.title)


class GuestGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guest_groups',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Guest Groups'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.title)


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='guests',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    events = models.ManyToManyField(
        GuestEvent,
        related_name='guests',
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
    has_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=2000, blank=True, null=True)
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
