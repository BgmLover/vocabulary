from django.urls import path

from . import views

app_name = 'words'
urlpatterns = [
    path('recite/', views.recite, name='recite'),
    path('get_recite_next/', views.get_recite_next_word, name='get_recite_next_word'),
    path('manage/', views.manage, name='manage'),
    path('finish_recite/', views.finish_recite, name='finish_recite'),
]
