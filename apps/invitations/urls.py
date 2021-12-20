from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.invitations.views import InvitationViewSet, AcceptInvite, UpdateWeddingTeamProfilePicture, WeddingsInvitedTo


router = DefaultRouter()
router.register(r'invitations', InvitationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accept_invite/', AcceptInvite.as_view()),
    path('update_wedding_team_profile_picture/', UpdateWeddingTeamProfilePicture.as_view()),
    path('weddings_invited_to/', WeddingsInvitedTo.as_view()),
]
