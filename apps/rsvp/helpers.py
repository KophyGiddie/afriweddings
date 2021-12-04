from apps.rsvp.models import RSVPQuestion
from django.core.exceptions import ValidationError


def get_rsvp_question_name(question, wedding):
    """
    Returns an rsvp question

    """
    try:
        myquestion = RSVPQuestion.objects.get(question=question, wedding=wedding)
        return myquestion
    except (RSVPQuestion.DoesNotExist, ValidationError):
        return None


def create_rsvp_question(question, mywedding, myuser):
    """
    Creates an rsvp question

    """
    myquestion = RSVPQuestion.objects.create(
        question=question,
        wedding=mywedding,
        created_by=myuser
    )
    return myquestion
