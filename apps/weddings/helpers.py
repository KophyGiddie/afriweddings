from apps.weddings.models import WeddingRole, Wedding
from django.core.exceptions import ValidationError
from apps.budget.models import BudgetCategory
from decimal import Decimal
import random


def get_role_by_name(role, wedding):
    try:
        WeddingRole.objects.get(role=role, wedding=wedding)
        return True
    except (WeddingRole.DoesNotExist, ValidationError):
        return None


def generate_slug(mywedding):
    print ('slug')


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
