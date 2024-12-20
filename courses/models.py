from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses'
    )

    def __str__(self):
        return self.name
