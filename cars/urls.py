from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('createcar', views.createcar, name='createcar'),
    path('createcarsave', views.createcarsave, name='createcarsave'),
    path('readcar', views.readcar, name='readcar'),
    path('updatecar', views.updatecar, name='updatecar'),
    path('updatecarsave', views.updatecarsave, name='updatecarsave'),
    path('deletecar', views.deletecar, name='deletecar'),
    path('deletecarsave/', views.deletecarsave, name='deletecarsave'),
    path('searchcar', views.searchcar, name='searchcar'),
    path('searchcarsave/', views.searchcarsave, name='searchcarsave'),
    path('help', views.help, name='help'),
]