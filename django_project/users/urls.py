from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path(r'<str:user_name>/index', views.index_login, name='index_login'),
    path(r'sign_up/', views.sign_up, name='sign_up'),
    path(r'sign_in/', views.sign_in, name='sign_in'),
    path(r'sign_out/', views.sign_out, name='sign_out'),
    path(r'users/sign_in/', views.sign_in, name='re_sign_in'),
    path(r'users/logout/', views.sign_out, name='sign_out')]
