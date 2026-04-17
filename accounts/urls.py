from django.urls import path
from .views import CreateAdminView, AdminLoginView, AddPersonView, logout_view

urlpatterns = [
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('logout/', logout_view, name='logout'),
    path('persons/add/', AddPersonView.as_view(), name='add-person'),
]
