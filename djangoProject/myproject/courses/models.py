# courses/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses', default=1)  # 设置默认值为1，假设这是管理员用户的ID
    # 其他字段...

    def __str__(self):
        return self.name