# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('changePassword/', views.change_password, name='change_password'),
    path('updateStudentProfile/', views.update_student_profile, name='update_student_profile'),
    path('showStudentProfile/', views.show_student_profile, name='show_student_profile'),
    path('updateTeacherProfile/', views.update_teacher_profile, name='update_teacher_profile'),
    path('showTeacherProfile/', views.show_teacher_profile, name='show_teacher_profile')
]

