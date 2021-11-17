from django.contrib import admin
from django.urls import path
from afriweddings.views import home, populate_default_checklist, populate_default_schedules
from django.conf.urls import include, handler500, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/', include('apps.budget.urls',)),
    path('api/v1.0/', include('apps.checklists.urls',)),
    path('api/v1.0/', include('apps.guests.urls',)),
    path('api/v1.0/', include('apps.invitations.urls',)),
    path('api/v1.0/prerequisites/', include('apps.prerequisites.urls',)),
    path('api/v1.0/rsvp/', include('apps.rsvp.urls',)),
    path('api/v1.0/seating/', include('apps.seating.urls',)),
    path('api/v1.0/users/', include('apps.users.urls',)),
    path('api/v1.0/', include('apps.weddings.urls',)),
    path('', home),
    path('populate_default_schedules/', populate_default_schedules),
    path('populate_default_checklist/', populate_default_checklist),
]

handler500 = 'afriweddings.views.handler500'

handler404 = 'afriweddings.views.handler404'

admin.site.site_header = 'Afriweddings Backend'
