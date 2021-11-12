from django.db import models
from apps.weddings.models import Wedding
from apps.guests.models import Guest
from django.conf import settings
import uuid


class SeatingTable(models.Model):
    """
    Model for seating tables

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='seating_tables',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='seating_tables',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    table_capacity = models.IntegerField(default=0)
    seats_assigned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Seating Table'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.name)


class SeatingChart(models.Model):
    """
    Model for seating chart configuration

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(
        SeatingTable,
        related_name='chart',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    guest = models.ForeignKey(
        Guest,
        related_name='chart',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    seat_number = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Seating Chart'
        ordering = ('-created_at',)

    def __str__(self):
        return 'Seat Number - %s' % (self.seat_number)
