from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.guests.views import GuestEventViewSet, GuestGroupViewSet, GuestViewSet


router = DefaultRouter()
router.register(r'guest_events', GuestEventViewSet)
router.register(r'guest_groups', GuestGroupViewSet)
router.register(r'guests', GuestViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
