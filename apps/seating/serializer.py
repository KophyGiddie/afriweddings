from rest_framework import serializers


class SeatingTableSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    table_capacity = serializers.CharField()
    seats_assigned = serializers.CharField()