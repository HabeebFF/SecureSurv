from django.urls import path
from .views import DashboardSummaryView, DetectionTrendsView, TopDetectedPersonsView, CameraActivityView, HourlyActivityView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('trends/', DetectionTrendsView.as_view(), name='detection-trends'),
    path('top-persons/', TopDetectedPersonsView.as_view(), name='top-detected-persons'),
    path('camera-activity/', CameraActivityView.as_view(), name='camera-activity'),
    path('hourly/', HourlyActivityView.as_view(), name='hourly-activity'),
]
