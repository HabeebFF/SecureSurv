from django.urls import path
from .views import UpdateLocationView, ToggleTrackingView, ActiveLocationsView

urlpatterns = [
    path('update-location/', UpdateLocationView.as_view(), name='update-location'),
    path('toggle/', ToggleTrackingView.as_view(), name='toggle-tracking'),
    path('active-locations/', ActiveLocationsView.as_view(), name='active-locations'),
]
