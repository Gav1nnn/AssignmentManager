# assignments/views.py

from django.shortcuts import render
from .models import Assignment  # 假设你有一个 Assignment 模型

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})