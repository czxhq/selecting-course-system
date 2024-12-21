# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.get_messages, name='get_messages'),
    path('courses/', views.get_courses, name='get_courses'),
    path('courseSelect/', views.course_details, name='course_details'),
    path('teacherCourses/', views.get_teacher_courses, name='get_teacher_courses'),
    path('creditProgress/', views.get_credit_progress, name='get_credit_progress'),
]
