from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.seating.views import SeatingTableViewSet, SeatingChartViewSet

router = DefaultRouter()
router.register(r'seating_tables', SeatingTableViewSet)
router.register(r'seating_chart', SeatingChartViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
