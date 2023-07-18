from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', views.not_authorized, name='not_authorized'),
    path('api-token-auth/', views.obtain_authentication_token, name='obtain_authentication_token'),
    path('airline/', views.create_airline, name='create_airline'),
    path('airline/update/<int:airline_id>/', views.update_airline, name='update_airline'),
    path('airline/retrieve/<int:airline_id>/', views.retrieve_airline, name='retrieve_airline'),
    path('airline/list/', views.list_airlines, name='list_airlines'),
    path('aircraft/', views.create_aircraft, name='create_aircraft'),
    path('aircraft/update/<int:aircraft_id>/', views.update_aircraft, name='update_aircraft'),
    path('aircraft/retrieve/<int:aircraft_id>/', views.retrieve_aircraft, name='retrieve_aircraft'),
    path('aircraft/delete/<int:aircraft_id>/', views.delete_aircraft, name='delete_aircraft'),
    path('airline/delete/<int:airline_id>/', views.delete_airline, name='delete_airline'),
]