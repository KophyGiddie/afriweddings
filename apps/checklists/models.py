from django.db import models
from apps.weddings.models import Wedding
from django.conf import settings
import uuid


class ChecklistCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Checklist Category'
        ordering = ('title',)

    def __str__(self):
        return '%s' % (self.title)


class ChecklistSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    priority = models.CharField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Default Checklist Schedule'
        ordering = ('priority',)

    def __str__(self):
        return '%s' % (self.name)


class Checklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ChecklistCategory,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wedding',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    schedule = models.ForeignKey(
        ChecklistSchedule,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_essential = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    title = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    note = models.CharField(max_length=4000, blank=True, null=True)
    priority = models.CharField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)