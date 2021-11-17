from rest_framework import serializers


class GuestEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    num_of_guests = serializers.IntegerField()


class GuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    num_of_guests = serializers.IntegerField()
