from django.db import models
from apps.weddings.models import Wedding
from apps.guests.models import Guest, GuestInvitation
import uuid
from django.conf import settings


class RSVPQuestion(models.Model):
    """
    Model for RSVP Questions displayed on the wedding page

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='rsvp',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.CharField(max_length=2000, blank=True, null=True)
    question_type = models.CharField(max_length=2000, blank=True, null=True)
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
        verbose_name_plural = 'RSVP Question'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.question)


class RSVP(models.Model):
    """
    Model for answers provided by guests on rsvp questions

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rsvp_question = models.ForeignKey(
        RSVPQuestion,
        related_name='rsvp',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    guest = models.ForeignKey(
        Guest,
        related_name='rsvp',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    guest_invitation = models.ForeignKey(
        GuestInvitation,
        related_name='rsvp',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    answer = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'RSVP'

    def __str__(self):
        return '%s' % (self.answer)
