from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.users.views import SignupUser, CurrentUserProfile, UpdatePartnerDetails

router = DefaultRouter()

urlpatterns = [
    path('signup/', SignupUser.as_view()),
    path('me/', CurrentUserProfile.as_view()),
    path('update_partner_details/', UpdatePartnerDetails.as_view()),
    path('', include(router.urls)),
]
