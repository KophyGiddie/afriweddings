from rest_framework import serializers
from apps.guests.serializer import GuestSerializer


class RSVPAnswerSerializer(serializers.Serializer):
    id = serializers.CharField()
    answer = serializers.CharField()


class RSVPQuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    question_type = serializers.CharField()
    answers = RSVPAnswerSerializer(many=True)


class RSVPSerializer(serializers.Serializer):
    id = serializers.CharField()
    answer = serializers.CharField()
    question = RSVPQuestionSerializer(many=False)
    guest = GuestSerializer(many=False)
