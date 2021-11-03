from django.db import models
from apps.weddings.models import Wedding
from apps.guests.models import Guest
import uuid


class RSVPQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.CharField(max_length=2000, blank=True, null=True)
    question_type = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'RSVP Question'
        ordering = ('question',)

    def __str__(self):
        return '%s' % (self.question)


class RSVP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rsvp_question = models.ForeignKey(
        RSVPQuestion,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    guest = models.ForeignKey(
        Guest,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    answer = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'RSVP'
        ordering = ('-id',)

    def __str__(self):
        return '%s' % (self.answer)
