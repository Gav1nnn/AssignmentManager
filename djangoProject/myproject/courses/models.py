# courses/models.py

from django.db import models
from django.conf import settings  

class Course(models.Model):
    course_name = models.CharField(max_length=100, null=True)  # 允许为空
    course_code = models.CharField(max_length=10, unique=True, null=True)  # 允许为空   确保课程序号唯一
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_created')  # 使用 settings.AUTH_USER_MODEL
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_joined', blank=True)
    
    def __str__(self):
        return f"{self.course_name} ({self.course_code})"


