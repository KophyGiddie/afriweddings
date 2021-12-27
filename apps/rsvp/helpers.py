from apps.rsvp.models import RSVPQuestion, RSVP, RSVPAnswer
from django.core.exceptions import ValidationError
from apps.guests.helpers import get_guest_public_invitation_by_id


def get_rsvp_question_name(question, wedding):
    """
    Returns an rsvp question

    """
    try:
        myquestion = RSVPQuestion.objects.get(question=question, wedding=wedding)
        return myquestion
    except (RSVPQuestion.DoesNotExist, ValidationError):
        return None


def get_rsvp_question_id(myid):
    """
    Returns an rsvp question

    """
    try:
        myquestion = RSVPQuestion.objects.get(id=myid)
        return myquestion
    except (RSVPQuestion.DoesNotExist, ValidationError):
        return None


def create_rsvp_question(question, mywedding, myuser, question_type, answers):
    """
    Creates an rsvp question

    """
    myquestion = RSVPQuestion.objects.create(
        question=question,
        question_type=question_type,
        wedding=mywedding,
        created_by=myuser
    )
    if question_type == 'BINARY':
        RSVPAnswer.objects.create(question=myquestion, answer='Yes')
        RSVPAnswer.objects.create(question=myquestion, answer='No')

    if question_type == 'MUTIPLE_CHOICE':
        myanswers = answers.split(',')
        for item in myanswers:
            RSVPAnswer.objects.create(question=myquestion, answer=item)

    return myquestion


def create_or_update_rsvp(guest_invitation_id, rsvp_question_id, answer):
    """
    Creates an rsvp question

    """
    guest_invitation = get_guest_public_invitation_by_id(guest_invitation_id)
    question = get_rsvp_question_id(rsvp_question_id)

    try:
        myrsvp = RSVP.objects.get(guest_invitation=guest_invitation, rsvp_question=question)
        myrsvp.answer = answer
        myrsvp.save()
    except RSVP.DoesNotExist:
        myrsvp = RSVP.objects.create(
            rsvp_question=question,
            guest=guest_invitation.guest,
            guest_invitation=guest_invitation,
            answer=answer
        )
        return myrsvp
