from django.db import models
from apps.weddings.models import Wedding
from django.conf import settings
import uuid


class ChecklistCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='checlist_category',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='checklist_category',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    identifier = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Checklist Category'
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.name)


class ChecklistSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='checklist_schedule',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='checklist_schedule',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    identifier = models.CharField(max_length=2000, blank=True, null=True)
    name = models.CharField(max_length=2000, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Checklist Schedule'
        ordering = ('priority',)

    def __str__(self):
        return '%s' % (self.name)


class Checklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=2000, blank=True, null=True)
    wedding = models.ForeignKey(
        Wedding,
        related_name='checklist',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ChecklistCategory,
        related_name='checklist',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='checklist',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    schedule = models.ForeignKey(
        ChecklistSchedule,
        related_name='checklists',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    time_done = models.DateTimeField(blank=True, null=True)
    is_essential = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    title = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    note = models.CharField(max_length=4000, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Checklist'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.name)