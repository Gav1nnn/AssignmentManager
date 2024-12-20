# myproject/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from captcha.views import captcha_refresh, captcha_image

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),  # Debug Toolbar
    path('admin/', admin.site.urls),  # Django 管理后台
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # 用户账户相关URL
    path('captcha/', include('captcha.urls')),  # 验证码URL
    re_path(r'^captcha/', include('captcha.urls')),  # 验证码URL（正则表达式路径）
]