# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from captcha.views import captcha_refresh, captcha_image

urlpatterns = [
    # Debug Toolbar (仅在开发环境中使用)
    path('__debug__/', include('debug_toolbar.urls')),

    # Django 管理后台
    path('admin/', admin.site.urls),

    # 用户账户相关URL，包含命名空间 'accounts'
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # 课程相关URL，包含命名空间 'courses'
    path('courses/', include('courses.urls', namespace='courses')),

    # 作业相关URL，包含命名空间 'assignments'
    path('assignments/', include('assignments.urls', namespace='assignments')),

    # 验证码URL
    path('captcha/', include('captcha.urls')),
]