# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cancelCourse/', views.cancel_course, name='cancel_course'),
    path('allCourse/', views.all_course, name='enroll'),
    path('search/', views.search_courses, name='search_courses'),
    path('get/', views.get_course_details, name='get_course_details'),
    path('question/', views.publish_question, name='publish_question'),
    path('selectCourse/', views.enroll_course, name='enroll'),
    path('addReview/', views.add_review, name='add_review'),
]
