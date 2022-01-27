from django.db import models
import uuid


class Country(models.Model):
    """
    Model for saving all the allowed countries

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    identifier = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Country'
        ordering = ('name',)


class DefaultChecklistCategory(models.Model):
    """
    Model for storing the default checklist categories used in prepopulating the couples checklist

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Checklist Category'
        ordering = ('name',)


class DefaultBudget(models.Model):
    """
    Model for storing the default faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=2000, blank=True, null=True)
    total_budget = models.DecimalField(max_digits=9, decimal_places=2, default='5000')

    def __str__(self):
        return '%s' % (self.country)

    class Meta:
        verbose_name_plural = 'Default Budget'
        ordering = ('id',)


class DefaultRSVPQuestion(models.Model):
    """
    Model for storing the default faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.question)

    class Meta:
        verbose_name_plural = 'Default RSVP Question'
        ordering = ('id',)


class DefaultFAQ(models.Model):
    """
    Model for storing the default faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=2000, blank=True, null=True)
    answer = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.question)

    class Meta:
        verbose_name_plural = 'Default FAQ'
        ordering = ('id',)


class DefaultBudgetCategory(models.Model):
    """
    Model for storing the default faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Budget Category'
        ordering = ('id',)


class DefaultBudgetExpense(models.Model):
    """
    Model for storing the default faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    percentage = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(
        DefaultBudgetCategory,
        related_name='budget_expense',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Budget Expense'
        ordering = ('id',)


class DefaultChecklistSchedule(models.Model):
    """
    Model for storing the default checklist schedules used in prepopulating the couples checklist

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Checklist Schedule'
        ordering = ('priority',)


class DefaultChecklist(models.Model):
    """
    Model for storing the default checkliste used in prepopulating the couples checklist

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=2000, blank=True, null=True)
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
    intent = models.CharField(max_length=2000, blank=True, null=True)
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
        return '%s' % (self.title)


class DefaultWeddingRole(models.Model):
    """
    Model for storing the default roles for prepopulation

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Default Wedding Roles'
        ordering = ('name', )
