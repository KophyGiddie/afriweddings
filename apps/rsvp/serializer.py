from rest_framework import serializers


class RSVPQuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    question_type = serializers.CharField()


class RSVPSerializer(serializers.Serializer):
    id = serializers.CharField()
    answer = serializers.CharField()
    question = RSVPQuestionSerializer(many=False)
