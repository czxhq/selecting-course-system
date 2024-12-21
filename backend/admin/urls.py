# admin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('notifications/', views.publish_notifications, name='publish_notifications'),
    path('getNotifications/', views.get_notifications, name='get_notifications'),
    path('importStudent/', views.import_student, name='import_student'),
    path('importTeacher/', views.import_teacher, name='import_teacher'),
    path('reset/', views.reset_password, name='reset_password'),
    path('deleteTeacher/', views.delete_teacher, name='delete_teacher'),
    path('deleteStudent/', views.delete_student, name='delete_student'),
    path('getAllStudent/', views.get_all_students, name='get_all_student'),
    path('getAllTeacher/', views.get_all_teachers, name='get_all_teacher'),
    path('importBatchStudent/', views.import_batch_student, name='importBatchStudent'),
    path('importBatchTeacher/', views.import_batch_teacher, name='importBatchTeacher'),
    path('addMajor/', views.add_major, name='add_major'),
    path('getMajors/', views.get_majors, name='get_majors'),
    path('alterMajor/', views.alter_major, name='alter_major'),
    path('exportStudents/', views.export_students, name='delete_major'),
    path('exportTeachers/', views.export_teachers, name='export_students'),
]
