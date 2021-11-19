from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.guests.views import GuestEventViewSet, GuestGroupViewSet, ExpensePayments


router = DefaultRouter()
router.register(r'guest_events', GuestEventViewSet)
router.register(r'guest_groups', GuestGroupViewSet)


urlpatterns = [
    path('expense_payments/', ExpensePayments.as_view()),
    path('', include(router.urls)),
]
