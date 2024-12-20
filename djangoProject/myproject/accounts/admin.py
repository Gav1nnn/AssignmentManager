from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    pass  # 如果有额外字段或方法，可以在这里添加