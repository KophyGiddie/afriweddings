from django.db import models
from apps.weddings.models import Wedding, WeddingRole
from django.conf import settings
from utils import constants
import uuid


class Invitation(models.Model):
    """
    Model for all invitations sent out of the platform

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='invitation',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='invitation',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    profile_picture = models.FileField(upload_to=constants.PROFILE_PIC_DIR, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    invitation_code = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    user_role = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.CharField(max_length=200, blank=True, null=True)
    invitation_type = models.CharField(max_length=200, blank=True, null=True)
    invitee_role = models.ForeignKey(
        WeddingRole,
        related_name='invitation',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=200, blank=True, default="PENDING")
    email_sent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Invitation'
        ordering = ('-created_at',)

    def get_profile_picture(self):
        if self.profile_picture:
            myimage = self.profile_picture.url
        else:
            myimage = ''
        return myimage

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
