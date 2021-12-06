from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.rsvp.views import RSVPQuestionViewSet, SubmitRSVP


router = DefaultRouter()
router.register(r'rsvp_questions', RSVPQuestionViewSet)

urlpatterns = [
    path('rsvp/', SubmitRSVP.as_view()),
    path('', include(router.urls)),
]
