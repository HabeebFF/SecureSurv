from django.urls import path
from .views import RegisterCameraView, GetAllCamerasView

urlpatterns = [
    path('register/', RegisterCameraView.as_view(), name='register-camera'),
    path('', GetAllCamerasView.as_view(), name='get-all-cameras'),
]
