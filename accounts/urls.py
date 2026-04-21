from django.urls import path
from .views import CreateAdminView, AdminLoginView, AddPersonView, AddPersonPhotoView, GetAllUsersView, GetAllPersonsView, logout_view, ToggleWantedStatusView

urlpatterns = [
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('logout/', logout_view, name='logout'),
    path('users/', GetAllUsersView.as_view(), name='get-all-users'),
    path('persons/', GetAllPersonsView.as_view(), name='get-all-persons'),
    path('persons/add/', AddPersonView.as_view(), name='add-person'),
    path('persons/<int:person_id>/toggle-wanted/', ToggleWantedStatusView.as_view(), name='toggle-wanted-status'),
    path('persons/<int:person_id>/add-photo/', AddPersonPhotoView.as_view(), name='add-person-photo'),
]
