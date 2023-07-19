from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('submit', views.submit, name='submit'),
    path('result', views.getResult, name='result'),
    path('logout', views.logout, name='logout'),

]
