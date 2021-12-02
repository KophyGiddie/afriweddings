from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.guests.views import (
    GuestEventViewSet, GuestGroupViewSet, GuestViewSet,
    UpdateOnlineGuestInvitation, FetchPublicInvitationDetail
)


router = DefaultRouter()
router.register(r'guest_events', GuestEventViewSet)
router.register(r'guest_groups', GuestGroupViewSet)
router.register(r'guests', GuestViewSet)


urlpatterns = [
    path('update_online_guest_invitation/', UpdateOnlineGuestInvitation.as_view()),
    path('fetch_public_invitation_detail/', FetchPublicInvitationDetail.as_view()),

    path('', include(router.urls)),
]
