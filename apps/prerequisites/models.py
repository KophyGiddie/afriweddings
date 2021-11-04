from django.db import models
import uuid


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Country'
        ordering = ('name',)


class DefaultChecklistCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name_plural = 'Default Checklist Category'
        ordering = ('title',)


class DefaultChecklistSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Checklist Schedule'
        ordering = ('priority',)


class DefaultChecklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        DefaultChecklistCategory,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    schedule = models.ForeignKey(
        DefaultChecklistSchedule,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_essential = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    title = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    note = models.CharField(max_length=4000, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Default Checklist'
        ordering = ('priority',)

    def __str__(self):
        return '%s' % (self.name)


class DefaultWeddingRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Wedding Roles'
        ordering = ('name', )
