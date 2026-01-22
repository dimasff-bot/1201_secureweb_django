from django.urls import path
from . import views

urlpatterns = [
    # HTML pages (client)
    path('', views.index, name='index'),

    path('signin/', views.signin, name='signin'),
    path('profilesecure/', views.profilesecure, name='profilesecure'),

    path('createcar/', views.createcar, name='createcar'),
    path('createcarsave/', views.createcarsave, name='createcarsave'),

    path('readcar/', views.readcar, name='readcar'),

    path('updatecar/', views.updatecar, name='updatecar'),
    path('updatecarsave/', views.updatecarsave, name='updatecarsave'),

    path('deletecar/', views.deletecar, name='deletecar'),
    path('deletecarsave/', views.deletecarsave, name='deletecarsave'),

    path('searchcar/', views.searchcar, name='searchcar'),
    path('searchcarsave/', views.searchcarsave, name='searchcarsave'),

    path('help/', views.help, name='help'),

    # API (server)
    path('api/cars/', views.api_cars, name='api_cars'),
]
