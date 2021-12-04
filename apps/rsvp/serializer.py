from rest_framework import serializers


class RSVPQuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
