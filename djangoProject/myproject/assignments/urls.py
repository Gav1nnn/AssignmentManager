# assignments/urls.py

from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.assignment_list, name='list'),
    # 其他 URL 模式
]