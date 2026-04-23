from django.urls import path
from .views import ScanFrameView, DetectionListView

urlpatterns = [
    path('scan/', ScanFrameView.as_view(), name='scan-frame'),
    path('detections/', DetectionListView.as_view(), name='detection-list'),
]
