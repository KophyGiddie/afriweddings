from django.db import models
from apps.weddings.models import Wedding, WeddingRole
from django.conf import settings
import uuid


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    email = models.CharField(max_length=200, blank=True, null=True)
    invitation_code = models.CharField(max_length=200, blank=True, null=True)
    invitation_type = models.CharField(max_length=200, blank=True, null=True)
    invitee_role = models.ForeignKey(
        WeddingRole,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=200, blank=True, default="PENDING")
    email_sent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
