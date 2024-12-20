# courses/views.py

from django.shortcuts import render
from .models import Course  # 假设你有一个 Course 模型

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})