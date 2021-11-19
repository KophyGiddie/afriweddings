from rest_framework import serializers


class GuestEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    invited_guests = serializers.CharField()
    confirmed_guests = serializers.CharField()
    guests_cancelled = serializers.CharField()
    guests_pending = serializers.CharField()


class GuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()


class ExtendedGuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()


class GuestSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    num_of_guests = serializers.IntegerField()
