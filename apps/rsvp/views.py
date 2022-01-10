from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.rsvp.serializer import (
    RSVPQuestionSerializer, RSVPSerializer
)
from rest_framework.permissions import AllowAny
from utils.utilities import get_wedding
from apps.rsvp.models import RSVPQuestion, RSVP
from apps.rsvp.helpers import get_rsvp_question_name, create_rsvp_question, create_or_update_rsvp

# Create your views here.


class RSVPQuestionViewSet(viewsets.ModelViewSet):
    model = RSVPQuestion
    serializer_class = RSVPQuestionSerializer
    queryset = RSVPQuestion.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of created guest events

        """
        myqueryset = RSVPQuestion.objects.prefetch_related('answers').filter(wedding__id=request.user.wedding_id)
        serializer = RSVPQuestionSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a guest event

        """
        question = request.data.get('question', None)
        question_type = request.data.get('question_type', None)
        answers = request.data.get('answers', None)

        if not question:
            return Response(error_response("Please provide a question", '140'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)
        existing_question = get_rsvp_question_name(question, mywedding)

        if existing_question:
            return Response(error_response("this question already exist", '139'), status=HTTP_400_BAD_REQUEST)

        myquestion = create_rsvp_question(question, mywedding, request.user, question_type, answers)

        serializer = RSVPQuestionSerializer(myquestion, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        edits a guest event

        """
        myquestion = self.get_object()

        if request.data.get('question') and request.data.get('question') != '':
            myquestion.question = request.data.get('question')

        myquestion.save()

        serializer = RSVPQuestionSerializer(myquestion, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a guest event

        """
        myobject = self.get_object()
        if myobject.created_by == request.user:
            myobject.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class RSVPResponses(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        mywedding = get_wedding(request)
        myqueryset = RSVP.objects.select_related('guest', 'rsvp_question').filter(rsvp_question__wedding=mywedding).order_by('-created_at')
        serializer = RSVPSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class SubmitRSVP(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        guest_invitation_id = request.data.get('guest_invitation_id', None)
        rsvp_question_id = request.data.get('rsvp_question_id', None)
        answer = request.data.get('answer', None)

        create_or_update_rsvp(guest_invitation_id, rsvp_question_id, answer)

        return Response(success_response('Submitted Successfully'), status=HTTP_200_OK)


class BulkSubmitRSVP(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        for element in data:
            create_or_update_rsvp(element['guest_invitation_id'], element['rsvp_question_id'], element['answer'])

        return Response(success_response('Submitted Successfully'), status=HTTP_200_OK)