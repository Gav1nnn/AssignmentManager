# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('create/', views.create_course, name='create_course'),
    path('teacher_courses/', views.teacher_courses, name='teacher_courses'),
    path('student_courses/', views.student_courses, name='student_courses'),
    path('join_course/<int:course_id>/', views.join_course, name='join_course'),
    path('leave_course/<int:course_id>/', views.leave_course, name='leave_course'),
]


