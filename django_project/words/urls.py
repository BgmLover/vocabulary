from django.urls import path

from . import views

app_name = 'words'
urlpatterns = [
    path('recite/', views.recite, name='recite'),
    path('review/', views.review, name='review'),
    path('examine/', views.examine, name='examine'),
    path('manage/', views.manage, name='manage'),
    path('define_words/', views.define_words, name='define_words'),
    path('collect_words/', views.collect_words, name='collect_words'),
    path('get_recite_next/', views.get_recite_next_word, name='get_recite_next_word'),
    path('get_review_next/', views.get_review_next_word, name='get_review_next_word'),
    path('finish_recite/', views.finish_recite, name='finish_recite'),
    path('finish_review/', views.finish_review, name='finish_review'),
    path('finish_examine/', views.finish_examine, name='finish_examine'),
]
