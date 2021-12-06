from apps.weddings.models import WeddingRole, Wedding, WeddingFAQ, WeddingScheduleEvent
from apps.guests.models import GuestGroup
from apps.prerequisites.models import DefaultRSVPQuestion
from django.core.exceptions import ValidationError
from apps.budget.models import BudgetCategory
from decimal import Decimal
import random
from apps.rsvp.helpers import create_rsvp_question


def validate_slug(myslug):
    try:
        Wedding.objects.get(public_url=myslug)
        return True
    except (Wedding.DoesNotExist, ValidationError):
        return False


def get_wedding_by_public_url(public_url):
    try:
        mywedding = Wedding.objects.get(public_url=public_url)
        return mywedding
    except (Wedding.DoesNotExist, ValidationError):
        return False


def get_role_by_name(role, wedding):
    try:
        WeddingRole.objects.get(role=role, wedding=wedding)
        return True
    except (WeddingRole.DoesNotExist, ValidationError):
        return None


def get_wedding_schedule_event_by_id(myid):
    try:
        myevent = WeddingScheduleEvent.objects.get(id=myid)
        return myevent
    except (WeddingScheduleEvent.DoesNotExist, ValidationError):
        return None


def get_schedule_event_by_name(name, wedding):
    try:
        myevent = WeddingScheduleEvent.objects.get(name=name, wedding=wedding)
        return myevent
    except (WeddingScheduleEvent.DoesNotExist, ValidationError):
        return None


def get_faq_by_question(question, wedding):
    try:
        myfaq = WeddingFAQ.objects.get(question=question, wedding=wedding)
        return myfaq
    except (WeddingFAQ.DoesNotExist, ValidationError):
        return None


def generate_slug(mywedding):
    first_name = mywedding.author.first_name
    partner_name = mywedding.partner_first_name

    determiner = True
    while determiner:
        myslug = '%s-%s%s' % (first_name, partner_name, random.randint(5, 1000))
        myresponse = validate_slug(myslug)
        if not myresponse:
            determiner = False
            mywedding.public_url = myslug
            mywedding.save()


def create_wedding_roles(mywedding):
    roles = ['Groom',
             'Bride',
             'Other',
             'Wedding Planner',
             'Bestman',
             'Maid of Honour',
             'Groomsman',
             'Bridesmaid'
             ]

    for role in roles:
        WeddingRole.objects.create(role=role, is_default=True, wedding=mywedding)


def create_wedding(wedding_date, expected_guests, country, currency, partner_role,
                   partner_last_name, myuser, city, partner_first_name):
    """
    Creates a wedding

    """
    mywedding = Wedding.objects.create(
        wedding_date=wedding_date,
        expected_guests=expected_guests,
        country=country,
        currency=currency,
        partner_role=partner_role,
        partner_last_name=partner_last_name,
        partner_first_name=partner_first_name,
        author=myuser,
        city=city
    )
    return mywedding


def create_default_budget_categories(mywedding, request):
    categories = ["Planning",
                  "Ceremony",
                  "Reception",
                  "Photography and Video",
                  "Music",
                  "Bride accessories",
                  "Wedding Invitations",
                  "Health and Beauty",
                  "Legal processes",
                  "Jewellery",
                  "Honeymoon",
                  "Flowers and Decoration",
                  "Gift list",
                  "Transport",
                  "Groom accessories",
                  "Other"
                 ]

    for category in categories:
        BudgetCategory.objects.create(
            name=category,
            wedding=mywedding,
            total_estimated_cost=Decimal(random.randint(500, 5000)),
            total_final_cost=Decimal(0),
            total_paid=Decimal(0),
            total_pending=Decimal(0),
            currency=mywedding.currency,
            created_by=request.user
        )


def create_rsvp_questions(mywedding, request):
    myquestions = DefaultRSVPQuestion.objects.all()
    for item in myquestions:
        create_rsvp_question(item.question, mywedding, request.user)


def custom_create_guest_group(mywedding, name, is_wedding_creator, is_partner, request):
    GuestGroup.objects.create(
        name=name,
        full_group_name=name,
        is_wedding_partner=is_partner,
        is_default=True,
        is_wedding_author=is_wedding_creator,
        wedding_creator_name=mywedding.author.first_name,
        wedding_partner_name=mywedding.partner_first_name,
        wedding=mywedding,
        created_by=request.user,
        num_of_guests=0,
    )
    return True


def create_guest_groups(mywedding, request):
    custom_create_guest_group(mywedding, 'Mutual Friends', False, False, request)
    custom_create_guest_group(mywedding, 'Unassigned', False, False, request)
    # Create Wedding Creators Groups
    custom_create_guest_group(mywedding, 'Friends', True, False, request)
    custom_create_guest_group(mywedding, 'Family', True, False, request)
    custom_create_guest_group(mywedding, 'Co-Workers', True, False, request)

    # Create Partner Groups
    custom_create_guest_group(mywedding, 'Friends', False, True, request)
    custom_create_guest_group(mywedding, 'Family', False, True, request)
    custom_create_guest_group(mywedding, 'Co-Workers', False, True, request)
