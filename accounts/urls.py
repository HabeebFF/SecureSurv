from django.urls import path
from .views import CreateAdminView, AdminLoginView

urlpatterns = [
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
]
