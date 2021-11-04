from django.contrib import admin
from django.urls import path
from afriweddings.views import home, populate_checklist, populate_schedules
from django.conf.urls import include, handler500, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/budget/', include('apps.budget.urls',)),
    path('api/v1.0/checklists/', include('apps.checklists.urls',)),
    path('api/v1.0/guests/', include('apps.guests.urls',)),
    path('api/v1.0/invitations/', include('apps.invitations.urls',)),
    path('api/v1.0/prerequisites/', include('apps.prerequisites.urls',)),
    path('api/v1.0/rsvp/', include('apps.rsvp.urls',)),
    path('api/v1.0/seating/', include('apps.seating.urls',)),
    path('api/v1.0/users/', include('apps.users.urls',)),
    path('api/v1.0/weddings/', include('apps.weddings.urls',)),
    path('', home),
    path('populate_schedules', populate_schedules),
    path('populate_checklist', populate_checklist),
]

handler500 = 'afriweddings.views.handler500'

handler404 = 'afriweddings.views.handler404'