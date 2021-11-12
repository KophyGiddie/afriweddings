from rest_framework import serializers


class ChecklistCategorySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class ChecklistScheduleSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    priority = serializers.IntegerField()


class ChecklistSerializer(serializers.Serializer):
    id = serializers.CharField()
    category = ChecklistCategorySerializer(many=False)
    schedule = ChecklistScheduleSerializer(many=False)
    note = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.IntegerField()
    title = serializers.CharField()
    is_essential = serializers.BooleanField()
    is_done = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class LimitedChecklistSerializer(serializers.Serializer):
    id = serializers.CharField()
    category = ChecklistCategorySerializer(many=False)
    schedule = ChecklistScheduleSerializer(many=False)
    note = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.IntegerField()
    title = serializers.CharField()
    is_essential = serializers.BooleanField()
    is_done = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class MasterChecklistScheduleSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    priority = serializers.IntegerField()
    checklists = LimitedChecklistSerializer(many=True)
