# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def is_student(self):
        return self.user_type == 'student'

    def is_teacher(self):
        return self.user_type == 'teacher'

