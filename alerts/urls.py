from django.urls import path
from .views import GetAllAlertsView

urlpatterns = [
    path('', GetAllAlertsView.as_view(), name='get-all-alerts'),
]
