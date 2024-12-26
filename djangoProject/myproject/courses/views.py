# courses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # 设置创建课程的教师
            course.save()
            return redirect('courses:teacher_courses')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def teacher_courses(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'courses/teacher_courses.html', {'courses': courses})

@login_required
def student_courses(request):
    all_courses = Course.objects.all()
    user_courses = request.user.courses_joined.all()  # 获取已加入的课程
    return render(request, 'courses/student_courses.html', {
        'all_courses': all_courses,
        'user_courses': user_courses,
    })

@login_required
def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)  # 学生加入课程
    return redirect('courses:student_courses')

@login_required
def leave_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.remove(request.user)  # 学生退出课程
    return redirect('courses:student_courses')




