from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.guests.views import (
    GuestEventViewSet, GuestGroupViewSet, GuestViewSet,
    UpdateOnlineGuestInvitation,
    SearchPublicGuest, GetGuestEventInvitations, BulkUploadGuestList,
    VerifyGuestToken, UpdateCompanionInfo
)

router = DefaultRouter()
router.register(r'guest_events', GuestEventViewSet)
router.register(r'guest_groups', GuestGroupViewSet)
router.register(r'guests', GuestViewSet)


urlpatterns = [
    path('update_online_guest_invitation/', UpdateOnlineGuestInvitation.as_view()),
    path('update_companion_details/', UpdateCompanionInfo.as_view()),
    path('search_public_guest/', SearchPublicGuest.as_view()),
    path('verify_guest_token/', VerifyGuestToken.as_view()),
    path('bulk_upload_guest_list/', BulkUploadGuestList.as_view()),
    path('get_guest_event_invitations/', GetGuestEventInvitations.as_view()),
    path('', include(router.urls)),
]
