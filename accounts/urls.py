from django.urls import path
from .views import CreateAdminView, AdminLoginView, AddPersonView, GetAllUsersView, GetAllPersonsView, logout_view

urlpatterns = [
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('logout/', logout_view, name='logout'),
    path('users/', GetAllUsersView.as_view(), name='get-all-users'),
    path('persons/', GetAllPersonsView.as_view(), name='get-all-persons'),
    path('persons/add/', AddPersonView.as_view(), name='add-person'),
]
