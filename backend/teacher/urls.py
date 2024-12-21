# teacher/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('publishCourse/', views.publish_course, name='publish_course'),
    path('notifications/', views.publish_notice, name='publish_notice'),
    path('alterCourse/', views.alter_course, name='alter_course'),
    path('deleteCourse/', views.delete_course, name='delete_course'),
    path('answer/', views.answer_question, name='answer_question'),
    path('question/', views.get_questions, name='get_questions'),
    path('enrollStudents/', views.enroll_students, name='enroll_students'),
    path('exportStudents/', views.export_students, name='export_student'),

]
