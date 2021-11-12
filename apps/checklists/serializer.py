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
    checklists = serializers.SerializerMethodField('get_checklists')

    def get_checklists(self, obj):
        is_done = self.context['request'].data.get('is_done')
        is_essential = self.context['request'].data.get('is_essential')
        category_id = self.context['request'].data.get('category_id')

        if is_done and is_done != '':
            myusers = obj.checklists.filter(is_done=is_done)

        if is_essential and is_essential != '':
            myusers = obj.checklists.filter(is_essential=is_essential)

        if category_id and category_id != '':
            myusers = obj.checklists.filter(category__id=category_id)

        serializer = LimitedChecklistSerializer(instance=myusers, many=True)
        return serializer.data

