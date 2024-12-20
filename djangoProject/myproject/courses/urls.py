# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    # 其他 URL 模式
]