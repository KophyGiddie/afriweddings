from rest_framework import serializers


class BudgetCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    currency = serializers.CharField()
    total_estimated_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_final_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_pending = serializers.DecimalField(max_digits=15, decimal_places=2)
    created_at = serializers.DateTimeField()


class BudgetExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    currency = serializers.CharField()
    estimated_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    final_cost = serializers.DecimalField(max_digits=15, decimal_places=2)
    paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending = serializers.DecimalField(max_digits=15, decimal_places=2)
    created_at = serializers.DateTimeField()


class ExpensePaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    paid_by = serializers.CharField()
    currency = serializers.CharField()
    payment_method = serializers.CharField()
    payment_due = serializers.DateField()
    payment_date = serializers.DateField()
    payment_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    is_paid = serializers.BooleanField()
    created_at = serializers.DateTimeField()