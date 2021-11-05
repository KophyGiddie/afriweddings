from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.weddings.views import WeddingViewSet


router = DefaultRouter()
router.register(r'weddings', WeddingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
