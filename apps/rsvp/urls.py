from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.rsvp.views import RSVPQuestionViewSet, SubmitRSVP, RSVPResponses


router = DefaultRouter()
router.register(r'rsvp_questions', RSVPQuestionViewSet)

urlpatterns = [
    path('rsvp/', SubmitRSVP.as_view()),
    path('rsvp_responses/', RSVPResponses.as_view()),
    path('', include(router.urls)),
]
