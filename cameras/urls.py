from django.urls import path
from .views import RegisterCameraView, GetAllCamerasView, UpdateCameraView, CameraFeedView

urlpatterns = [
    path('register/', RegisterCameraView.as_view(), name='register-camera'),
    path('', GetAllCamerasView.as_view(), name='get-all-cameras'),
    path('<int:camera_id>/update/', UpdateCameraView.as_view(), name='update-camera'),
    path('<int:camera_id>/feed/', CameraFeedView.as_view(), name='camera-feed'),
]
