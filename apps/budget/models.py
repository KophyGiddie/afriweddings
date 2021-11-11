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
        verbose_name_plural = 'Budget Category'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.name)


class BudgetExpense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        BudgetCategory,
        related_name='budget_expense',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='budget_expense',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    note = models.CharField(max_length=2000, blank=True, null=True)
    currency = models.CharField(max_length=2000, blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    final_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    paid = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    pending = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Budget Expense'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.name)


class ExpensePayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(
        BudgetExpense,
        related_name='payments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    paid_by = models.CharField(max_length=2000, blank=True, null=True)
    payment_method = models.CharField(max_length=2000, blank=True, null=True)
    payment_due = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=2000, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='payments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Expense Payment'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s' % (self.payment_amount)
