from rest_framework import serializers
from apps.guests.serializer import GuestSerializer


class SeatingTableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    table_capacity = serializers.CharField()
    seats_assigned = serializers.CharField()


class SeatingChartSerializer(serializers.Serializer):
    id = serializers.CharField()
    guest = GuestSerializer(many=False)
    table = SeatingTableSerializer(many=False)
    seat_number = serializers.CharField()
