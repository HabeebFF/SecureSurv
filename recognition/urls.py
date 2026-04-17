from django.urls import path
from .views import ScanFrameView

urlpatterns = [
    path('scan/', ScanFrameView.as_view(), name='scan-frame'),
]
