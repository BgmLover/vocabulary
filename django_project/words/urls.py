from django.urls import path

from . import views

app_name = 'words'
urlpatterns = [
    path('recite/', views.recite, name='recite'),
    path('manage/', views.manage, name='manage'),
]
