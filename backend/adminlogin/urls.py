# admin_login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='login'),

]
