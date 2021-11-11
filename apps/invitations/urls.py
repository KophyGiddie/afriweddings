from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.invitations.views import InvitationViewSet, AcceptInvite


router = DefaultRouter()
router.register(r'invitations', InvitationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accept_invite/', AcceptInvite.as_view()),
]
