from django.db import models
from apps.weddings.models import Wedding
from django.conf import settings
import uuid


class BudgetCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='budget_categories',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='budget_categories',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    currency = models.CharField(max_length=2000, blank=True, null=True)
    total_estimated_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_final_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_paid = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_pending = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Checklist Category'
        ordering = ('title',)

    def __str__(self):
        return '%s' % (self.title)


class BudgetExpense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        BudgetCategory,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    currency = models.CharField(max_length=2000, blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    paid = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    pending = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Default Checklist Schedule'
        ordering = ('priority',)

    def __str__(self):
        return '%s' % (self.name)

