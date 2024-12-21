# teacherlogin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_login, name='login'),
]
